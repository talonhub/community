"""Acting on windows: close, minimize, restore, maximize, snap, lay out, move to a
screen or desktop; finishing a layout (raise, then focus the last window); focus
holding; virtual desktops."""

import time
from talon import actions, app, cron, ui
from ...egui_kit import native
from . import dwm_thumbnails as dwm
from ..windows import virtual_desktops as vd
from . import window_icons
from .config import CLOSE_CHECKS, HOLD_FOCUS_SECONDS
from .model import AppGroup, Entry, screen_number, screen_rects, screen_work_rects


class WindowOpsMixin:
    """Switcher methods: see the module docstring. Mixed into Switcher, whose state they use."""

    def _finish_layout(self, entries: list[Entry]):
        """After a layout: close the switcher, bring the layout's windows to the front
        and focus its last window. The switcher hands the focus over while it still
        has it (Windows only lets the foreground window do that), and the window the
        switcher was opened from doesn't get it back."""
        last = entries[-1]
        for entry in entries[:-1]:
            if dwm.is_minimized(entry.hwnd):
                dwm.restore(entry.hwnd)
            dwm.raise_quietly(entry.hwnd)
        if dwm.is_minimized(last.hwnd):
            dwm.restore(last.hwnd)
        native.set_foreground(last.hwnd)
        self.hide()

        def check():
            if native.foreground() != last.hwnd:
                try:
                    actions.user.switcher_focus_window(last.window)
                except Exception:
                    native.set_foreground(last.hwnd)

        cron.after("300ms", check)

    def _activate(self, entries: list[Entry]):
        """Close the switcher and focus `entries` in turn, so the last ends up on top."""
        if entries[-1].away and entries[-1].desktop is not None:
            # Activating a window doesn't reliably switch to its desktop by itself.
            try:
                vd.switch_to(entries[-1].desktop)
            except OSError as e:
                print(f"thumbnail_switcher: switching desktop failed: {e}")
        for entry in entries:
            if dwm.is_minimized(entry.hwnd):
                dwm.restore(entry.hwnd)
        # Focus before hiding, see cancel(); the switcher may still be foreground and
        # so allowed to hand focus over.
        native.set_foreground(entries[0].hwnd)
        self.hide()
        # Raise the others quickly; only the last one needs to end up with focus.
        for entry in entries[1:]:
            native.set_foreground(entry.hwnd)
        last = entries[-1]
        try:
            actions.user.switcher_focus_window(last.window)
        except Exception as e:
            print(f"thumbnail_switcher: focusing {last.title!r} failed: {e!r}")
            last.window.focus()

    def _entries(self, indices: list[int], entries: list[Entry] | None) -> list[Entry]:
        return self.entries_at(indices) if entries is None else entries

    def close_windows(self, indices: list[int] = (), entries: list[Entry] | None = None):
        """Ask these windows to close; their tiles go once they have (see sync)."""
        for entry in self._entries(indices, entries):
            for window in getattr(entry, "windows", [entry]):
                dwm.request_close(window.hwnd)
        # Talon's win_close usually arrives first; these catch windows that took a
        # while, e.g. after asking to save.
        for delay in CLOSE_CHECKS:
            cron.after(delay, self.sync)

    def minimize_windows(self, indices: list[int] = (), entries: list[Entry] | None = None):
        """Minimize these windows; their tiles switch to the app icon."""
        for entry in self._entries(indices, entries):
            dwm.minimize_quietly(entry.hwnd)
        self.sync()

    def restore_windows(self, indices: list[int] = (), entries: list[Entry] | None = None):
        """Restore these minimized windows behind the switcher."""
        for entry in self._entries(indices, entries):
            if dwm.is_minimized(entry.hwnd):
                dwm.restore_quietly(entry.hwnd)
        self.sync()

    def maximize_window(self, index: int):
        """Maximize the window behind the switcher."""
        entries = self.entries_at([index])
        if not entries:
            return
        # Maximizing always activates the window; take focus straight back.
        self._hold_focus()
        dwm.maximize(entries[0].hwnd)
        self._take_focus()
        self.sync()

    def snap_window(self, index: int, position):
        """Snap the window to a community snap position."""
        self.layout_windows([index], [position])

    def layout_windows(self, indices: list[int], positions: list, entries: list[Entry] | None = None):
        """Snap windows to positions pairwise.

        Positions are window_snap.py position objects or the names of its positions.
        """
        entries = self._entries(indices, entries)[: len(positions)]
        if not entries:
            return
        self._hold_focus()
        for entry, position in zip(entries, positions):
            try:
                # A window on another desktop comes here first: snapped there, it
                # couldn't be seen.
                if entry.away and self.current_desktop is not None:
                    vd.move_window(entry.hwnd, next(d.guid for d in self.desktops if d.guid.key() == self.current_desktop))
                    entry.away = False
                # Snapping sets the window's rect, which a minimized or maximized
                # window ignores.
                dwm.make_normal(entry.hwnd)
                if isinstance(position, str):
                    actions.user.snap_window_to_position(position, entry.window)
                else:
                    actions.user.snap_window(position, entry.window)
            except Exception as e:
                print(f"thumbnail_switcher: snapping {entry.title!r} failed: {e!r}")
        if len(entries) > 1:
            # A layout: show the result, the layout's last window focused.
            self._finish_layout(entries)
            return
        self._take_focus()
        self.sync()

    def move_to_screen(self, index: int, screen: int | None = None, offset: int = 0):
        """Move the window on tile `index` to screen `screen`, or `offset` screens along;
        for an app (apps view), all its windows."""
        entries = self.entries_at([index])
        if not entries:
            return
        self._hold_focus()
        for entry in getattr(entries[0], "windows", entries):
            self._move_window_to_screen(entry, screen, offset)
        self._take_focus()
        self.sync()

    def _move_window_to_screen(self, entry: Entry, screen: int | None, offset: int):
        """Move one window to another screen, keeping its place relative to the screen's
        usable area, like community's screen moves; but without focusing it (those only
        act on the active window). Screens are numbered like the screen commands."""
        screens = screen_rects()
        areas = screen_work_rects()
        source = entry.screen_number or screen_number(entry.hwnd, screens)
        if source is None or len(areas) < 2:
            return
        target = screen if screen is not None else (source - 1 + offset) % len(areas) + 1
        if not 0 < target <= len(areas) or target == source:
            return
        window = entry.window
        dwm.unminimize(entry.hwnd)
        maximized = dwm.is_maximized(entry.hwnd)
        dwm.make_normal(entry.hwnd)
        # From Windows: Talon's rect of a just-restored window can still be its
        # minimized, off-screen one.
        s, d, r = areas[source - 1], areas[target - 1], dwm.frame_rect(entry.hwnd)
        scale_x = (d[2] - d[0]) / (s[2] - s[0])
        scale_y = (d[3] - d[1]) / (s[3] - s[1])
        window.rect = ui.Rect(
            round(d[0] + (r[0] - s[0]) * scale_x),
            round(d[1] + (r[1] - s[1]) * scale_y),
            round((r[2] - r[0]) * scale_x),
            round((r[3] - r[1]) * scale_y),
        )
        if maximized:
            window.maximized = True

    def move_to_desktop(
        self, indices: list[int], number: int | None = None, offset: int = 0, entries: list[Entry] | None = None
    ):
        """Move windows to virtual desktop `number`, or `offset` desktops along."""
        if not vd.available():
            app.notify("Thumbnail switcher", f"Can't move windows between desktops: {vd.unavailable_reason()}")
            return
        with self.lock:
            desktops = list(self.desktops)
        for entry in self._entries(indices, entries):
            target = number if number is not None else (entry.desktop_number or 1) + offset
            desktop = next((d for d in desktops if d.number == target), None)
            if desktop is None:
                app.notify("Thumbnail switcher", f"There is no desktop {target}")
                continue
            try:
                vd.move_window(entry.hwnd, desktop.guid)
            except OSError as e:
                print(f"thumbnail_switcher: moving {entry.title!r} to desktop {target} failed: {e}")
        self._take_focus()
        self.sync()

    def move_app_to_desktop(self, group: AppGroup, number: int):
        """Move every window of an app to desktop `number`."""
        desktop = next((d for d in self.desktops if d.number == number), None)
        if desktop is None:
            return
        for window in group.windows:
            try:
                vd.move_window(window.hwnd, desktop.guid)
            except OSError as e:
                print(f"thumbnail_switcher: moving {window.title!r} failed: {e}")
        self._take_focus()
        self.sync()

    def move_to_new_desktop(self, index: int):
        """Create a virtual desktop and move the window there."""
        try:
            desktop = vd.create_desktop()
        except OSError as e:
            app.notify("Thumbnail switcher", f"Couldn't create a desktop: {e}")
            return
        with self.lock:
            self.desktops, self.current_desktop = self._read_desktops()
        self.move_to_desktop([index], number=desktop.number)

    def _read_desktops(self) -> tuple[list[vd.Desktop], bytes | None]:
        try:
            desktops = vd.desktops()
            current = vd.current_desktop()
        except OSError as e:
            print(f"thumbnail_switcher: reading virtual desktops failed: {e}")
            return [], None
        return desktops, (current.guid.key() if current else None)

    def _set_desktop(self, entry: Entry, desktops: list[vd.Desktop], current: bytes | None, previews: bool):
        """Record which desktop the window is on; fetches its icon if that makes it iconic."""
        guid = vd.window_desktop(entry.hwnd)
        entry.desktop = guid
        entry.desktop_key = guid.key() if guid else None
        entry.desktop_number = next((d.number for d in desktops if d.guid.key() == entry.desktop_key), None)
        entry.away = entry.desktop_key is not None and current is not None and entry.desktop_key != current
        if previews and entry.away and entry.icon is None:
            entry.icon = entry._find_icon(entry.window, window_icons.ICON_SIZE)

    def _hold_focus(self):
        self.hold_focus_until = time.monotonic() + HOLD_FOCUS_SECONDS

    def _take_focus(self):
        if self.showing and self.hwnd is not None and native.foreground() != self.hwnd:
            if self.menu is not None and self.popup.has_focus():
                return  # the open menu's popup has it
            native.set_foreground(self.hwnd)
