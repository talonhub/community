"""The switcher's native window and the windows it shows: following window events,
sync, DWM thumbnails, the tick (focus, re-pinning geometry), the menu's popup window."""

import ctypes
import time
from talon import ui
from ...egui_kit import native, popup
from . import dwm_thumbnails as dwm
from . import window_icons
from .config import APP_ICON_PIXELS, APP_MODES, GUARD_EVERY_TICKS, SYNC_EVERY_TICKS
from .model import Entry, is_switchable, screen_number, screen_rects
from .sources import is_candidate


class WindowHostMixin:
    """Switcher methods: see the module docstring. Mixed into Switcher, whose state they use."""

    def _on_window_event(self, window: ui.Window):
        """A Talon window event: catch up with whatever changed."""
        if not self.showing:
            return
        with self.lock:
            known = any(e.hwnd == window.id for e in self.pool)
        if known:
            self.sync()
        else:
            self._maybe_add(window)

    def _maybe_add(self, window: ui.Window):
        """Add a window that appeared while the switcher is open."""
        if window.id == self.hwnd or not is_candidate(window):
            return
        entry = Entry(window, self.previews, APP_ICON_PIXELS if self.mode in APP_MODES else None)
        with self.lock:
            if not self.showing or any(e.hwnd == entry.hwnd for e in self.pool):
                return
            self.pool.append(entry)
            self._register_thumbnail(entry)
            self._refilter(keep_selection=True)
        self.refresh()

    def sync(self, repaint: bool = True):
        """Bring the tiles in line with the windows: drop closed ones, swap thumbnails
        and icons for minimized or restored ones, and pick up new titles.

        Repaints when anything changed, or always with `repaint`, so thumbnails of
        moved or resized windows get re-fitted.
        """
        if not self.showing:
            return
        with self.lock:
            pool = list(self.pool)
            previews = self.previews
        gone = {e.hwnd for e in pool if not native.is_window(e.hwnd) or not is_switchable(e.hwnd)}
        desktops, current = self._read_desktops()
        moved = {}
        for entry in pool:
            if entry.hwnd in gone:
                continue
            probe = Entry.__new__(Entry)
            probe.hwnd, probe.window, probe.icon, probe.title = entry.hwnd, entry.window, entry.icon, entry.title
            self._set_desktop(probe, desktops, current, previews)
            if (probe.desktop_key, probe.desktop_number, probe.away) != (entry.desktop_key, entry.desktop_number, entry.away):
                moved[entry.hwnd] = probe
        minimized = {}
        titles = {}
        icons = {}
        for entry in pool:
            if entry.hwnd in gone:
                continue
            state = dwm.is_minimized(entry.hwnd)
            if state != entry.minimized:
                minimized[entry.hwnd] = state
                if previews and state and entry.icon is None:
                    # Looked up outside the lock: it can take a moment.
                    icons[entry.hwnd] = entry._find_icon(entry.window, window_icons.ICON_SIZE)
            title = dwm.window_text(entry.hwnd)
            if title and title != entry.title:
                titles[entry.hwnd] = title
        desktops_changed = [d.guid.key() for d in desktops] != [d.guid.key() for d in self.desktops] or current != self.current_desktop
        screens = screen_rects()
        placed = {e.hwnd: screen_number(e.hwnd, screens) for e in pool if e.hwnd not in gone}
        if len(screens) != self.screen_count or any(placed[e.hwnd] != e.screen_number for e in pool if e.hwnd in placed):
            with self.lock:
                self.screen_count = len(screens)
                for entry in self.pool:
                    if entry.hwnd in placed:
                        entry.screen_number = placed[entry.hwnd]
                self._refilter(keep_selection=True)
            self.refresh()
        if gone or minimized or titles or moved or desktops_changed:
            with self.lock:
                self.desktops, self.current_desktop = desktops, current
                for entry in self.pool:
                    if entry.hwnd in moved:
                        probe = moved[entry.hwnd]
                        entry.desktop, entry.desktop_key = probe.desktop, probe.desktop_key
                        entry.desktop_number, entry.away = probe.desktop_number, probe.away
                        entry.icon = probe.icon
                    if entry.hwnd in minimized:
                        entry.minimized = minimized[entry.hwnd]
                        if entry.hwnd in icons:
                            entry.icon = icons[entry.hwnd]
                    if entry.hwnd in minimized or entry.hwnd in moved:
                        if entry.iconic:
                            self._unregister_thumbnail(entry.hwnd)
                        else:
                            self._register_thumbnail(entry)
                    if entry.hwnd in titles:
                        entry.set_title(titles[entry.hwnd])
                for hwnd in gone:
                    self._unregister_thumbnail(hwnd)
                self.pool = [e for e in self.pool if e.hwnd not in gone]
                # Marks go with closed windows, but not with ones that only drop out
                # for a moment (moving between desktops) and come back.
                self.marked = [h for h in self.marked if h not in gone or native.is_window(h)]
                self._refilter(keep_selection=True)
        if repaint or gone or minimized or titles or moved or desktops_changed:
            self.refresh()

    def _register_thumbnail(self, entry: Entry):
        """Give a visible window its DWM thumbnail; call with the lock held."""
        if not self.previews or entry.iconic or self.hwnd is None or entry.hwnd in self.thumbnails:
            return
        try:
            self.thumbnails[entry.hwnd] = dwm.Thumbnail(self.hwnd, entry.hwnd)
        except OSError as e:
            print(f"thumbnail_switcher: {entry.title!r}: {e}")

    def _unregister_thumbnail(self, hwnd: int):
        """Call with the lock held."""
        thumbnail = self.thumbnails.pop(hwnd, None)
        if thumbnail is not None:
            thumbnail.close()

    def _guess_ppp(self) -> float:
        """The scale of the monitor with the foreground window, as egui will use it (its
        effective DPI / 96; Talon's screen.scale can differ, e.g. 1.8 for 200%)."""
        try:
            monitor = dwm.user32.MonitorFromWindow(dwm.user32.GetForegroundWindow(), 2)  # MONITOR_DEFAULTTONEAREST
            dpi_x, dpi_y = ctypes.c_uint(), ctypes.c_uint()
            get_dpi = ctypes.windll.shcore.GetDpiForMonitor
            get_dpi.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
            # MDT_EFFECTIVE_DPI
            if get_dpi(monitor, 0, ctypes.byref(dpi_x), ctypes.byref(dpi_y)) == 0 and dpi_x.value:
                return dpi_x.value / 96
        except Exception:
            pass
        try:
            return ui.active_window().screen.scale
        except Exception:
            return 1.0

    def _tick(self):
        if not self.showing:
            return
        if self.hwnd is None:
            hwnd = self.host.find_hwnd()
            if hwnd is None:
                return
            self.hwnd = hwnd
            self._attach()
            return
        self.ticks += 1
        # Close when the user moves on to another window, like Alt+Tab; but not when
        # one of the switcher's own commands briefly activated a window.
        foreground = native.foreground()
        if foreground is not None and foreground == self.popup.host.hwnd:
            # A click on the menu's popup activates it despite WS_EX_NOACTIVATE (egui
            # takes the focus on a click): hand it straight back, keys go here. That
            # raises the switcher, so the popup goes back over it (they can overlap).
            native.set_foreground(self.hwnd)
            native.raise_topmost(self.popup.host.hwnd)
            foreground = self.hwnd
        has_focus = foreground == self.hwnd
        if has_focus:
            self.had_focus = True
        elif self.had_focus:
            if time.monotonic() < self.hold_focus_until:
                self._take_focus()
            else:
                self.hide()
                return
        if self.ticks % SYNC_EVERY_TICKS == 0:
            # Talon has no event for minimizing and restoring.
            self.sync(repaint=False)
        if self.placement is not None:
            self._stack_overlays()
        if self.ticks % GUARD_EVERY_TICKS == 0 and self.target is not None:
            # winit may apply its own geometry after creation or on DPI changes.
            if native.hwnd_rect(self.hwnd) != self.target:
                native.move_hwnd(self.hwnd, self.target)

    def _place_menu_popup(self, request):
        """Show the menu's popup window for `request` ((x, y) where it opens, (w, h)),
        beside that point within the monitor's work area; None hides it."""
        if request is None or self.menu is None or not self.showing:
            self.popup.hide()
            return
        if self.hwnd is None:
            # Not attached yet: ask again on a later frame.
            self.menu_request = None
            self.refresh()
            return
        (x, y), size = request
        self.popup.show(popup.place((x, y, x, y), size, native.work_area(self.hwnd)))

    def _attach(self):
        """Position the native window and register a thumbnail for every entry."""
        native.move_hwnd(self.hwnd, self.target)
        self.host.focus()
        if native.foreground() != self.hwnd:
            native.set_foreground(self.hwnd)
        with self.lock:
            for entry in self.pool:
                # A minimized window's thumbnail is blank; its tile shows the icon.
                self._register_thumbnail(entry)
        # Thumbnails are placed from render, which knows the tile rectangles.
        self.refresh()

    def _clear_thumbnails(self):
        with self.lock:
            for thumbnail in self.thumbnails.values():
                thumbnail.close()
            self.thumbnails = {}
