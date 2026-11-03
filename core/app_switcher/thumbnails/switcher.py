"""The switcher: its state (guarded by one non-reentrant lock), showing and hiding, the
search and filters, views and sorting, selection and scrolling, selecting and
launching. Drawing, input, marks, the native window, menus, placement and window
operations are mixins (views, cells, input, textures, marks, window_host, menus,
placement, window_ops)."""

import threading
from typing import Any
import egui
from talon import app, cron, registry, settings, ui
from ...egui_kit.host import HostWindow
from ...egui_kit import native
from . import dwm_thumbnails as dwm
from ..windows import virtual_desktops as vd
from ..windows import app_identity
from . import launcher_apps
from .cells import CellsMixin
from .config import (
    APPS_MIN_HEIGHT,
    APP_ICON_PIXELS,
    APP_MODES,
    APP_TAG,
    COLUMN_HEADER_HEIGHT,
    DESK_TAG,
    DETAIL_ROW_HEIGHT,
    HEADER_HEIGHT,
    INDEX_LETTERS,
    PADDING,
    ROW_GAP,
    SCREEN_FILL,
    SCREEN_TAG,
    SEARCH_HEIGHT,
    SORTABLE,
    TICK_MS,
    WINDOW_DETAILS_MIN_WIDTH,
    WINDOW_EVENTS,
    WINDOW_TITLE,
)
from .input import InputMixin
from .marks import MarksMixin
from .menus import Menu, MenuMixin
from .model import (
    AppGroup,
    Chip,
    Entry,
    app_chip,
    group_apps,
    launch_id,
    launcher_letters,
    matches,
    resolve_app,
    screen_number,
    screen_rects,
    window_state,
)
from .placement import GridOverlay, Placement, PlacementMixin, SlotOverlay
from .sizing import choose_apps, choose_grid, choose_list
from .sources import all_windows
from .textures import TexturesMixin
from .views import ViewsMixin
from .window_host import WindowHostMixin
from .window_ops import WindowOpsMixin


class Switcher(ViewsMixin, CellsMixin, InputMixin, TexturesMixin, MarksMixin, WindowHostMixin, MenuMixin, PlacementMixin, WindowOpsMixin):
    def __init__(self, tag_context=None):
        # The Talon surface's Context, whose tags the switcher sets (see _update_tags).
        self.tag_context = tag_context
        self.lock = threading.Lock()
        # Every window the switcher opened with, and the ones the search lets through;
        # numbers, the selection and select() refer to `entries`.
        self.pool: list[Entry] = []
        self.entries: list[Entry] = []
        self.chip: Chip | None = None
        self.query = ""
        self.previews = True
        self.cols = 1
        # Scroll position of the tiles or rows, in egui points from the top.
        self.scroll = 0.0
        self.reveal_selected = False
        # Where the mouse was when the switcher opened, in points; see _pointer_moved.
        self.pointer_origin: tuple[int, int] | None = None
        self.target: tuple[int, int, int, int] | None = None
        # The window's rect before it grew to fit a menu; put back when the menu closes.
        self.menu_restore: tuple[int, int, int, int] | None = None
        # Where the marked bar's dropdowns open (page -> egui point), from the last frame.
        self.bar_anchors: dict[str, Any] = {}
        self.hwnd: int | None = None
        self.thumbnails: dict[int, dwm.Thumbnail] = {}
        # Icon textures, keyed by (hwnd, icon width). They are only created and dropped
        # inside render, on egui's thread: dropping one elsewhere may lack a GL context.
        self.textures: dict[tuple, egui.TextureHandle] = {}
        # Jump list entries' icons by entry: None while loading or when there's none.
        self.jump_icons: dict[tuple, Any] = {}
        self.selected = 0
        self.previous_foreground: int | None = None
        self.had_focus = False
        self.hold_focus_until = 0.0
        self.events_registered = False
        # Virtual desktops in order, and the key of the current one.
        self.desktops: list[vd.Desktop] = []
        # How many screens there are; their badges only show with more than one.
        self.screen_count = 1
        self.current_desktop: bytes | None = None
        self.placement: Placement | None = None
        self.overlay = SlotOverlay()
        self.grid_overlay = GridOverlay()
        self.menu: Menu | None = None
        # Marked windows (multi-select) in the order they were marked, by hwnd; they
        # stay marked while the search hides them. And the window a Shift range starts at.
        self.marked: list[int] = []
        self.mark_anchor: int | None = None
        # The launcher's installed apps, and how many running apps come first.
        self.launch_list: launcher_apps.LaunchList | None = None
        self.running_count = 0
        # The last frame's tile layout and sections (for row-wise keys and jumps), how
        # many rows a page holds, and a tile to scroll to the top (a letter jump).
        self.layout: list[tuple[int, int, int]] = []
        self.sections: list[tuple[int, str]] = []
        self.page_rows = 1
        self.scroll_to: int | None = None
        # The launcher as a details table (None: the setting decides on first use, then
        # the choice holds for the session); its sort column (None: running apps first
        # by recent use, then apps by name) and direction; the grid's columns.
        self.launcher_details: bool | None = None
        # The window list as a details table (a row per window), and its sort.
        self.window_details = False
        self.window_details_last = False
        self.window_sort: str | None = None
        self.window_sort_reverse = False
        # The running applications view as a details table (None: the setting decides
        # on first use, then the last choice sticks), and its sort.
        self.apps_details: bool | None = None
        self.apps_sort: str | None = None
        self.apps_sort_reverse = False
        self.launcher_sort: str | None = None
        self.launcher_sort_reverse = False
        self.grid_cols = 1
        # Spoken forms by running-list value and by launch id, for the details view.
        self.spoken_running: dict[str, list[str]] = {}
        self.spoken_launch: dict[str, list[str]] = {}
        # "windows": a tile per window; "apps": a tile per application; "launcher": a
        # tile per running app, then per installed app.
        self.mode = "windows"
        self.showing = False
        self.ticks = 0

        # Takes keyboard focus while showing, for the arrow keys, Enter and Escape.
        self.host = HostWindow(
            WINDOW_TITLE,
            self.render,
            tag="thumbnail_switcher",
            decorated=False,
            resizable=False,
            draggable=False,
            autosize=False,
            toplevel=True,
            focusable=True,
        )
        self.tick_job = cron.interval(f"{TICK_MS}ms", self._tick)

    # --- showing and hiding ---

    def show(
        self,
        windows: list[ui.Window],
        chip_windows: list[ui.Window] | None = None,
        chip_label: str = "",
        mode: str = "windows",
        window_details: bool = False,
    ):
        """Open with `windows`; with `chip_windows`, filtered to those behind an app chip.

        The window is sized for all of `windows`, so it doesn't jump around when the
        chip is removed or the search narrows things down. With `mode` "apps", there is
        a tile per application instead of per window.
        """
        if not windows:
            app.notify("Thumbnail switcher", "No windows")
            return
        self._clear_thumbnails()
        if not self.showing:
            self.previous_foreground = native.foreground()
        work = native.foreground_work_area()
        # Physical pixels per egui point; the window is not up yet, so guess from the
        # monitor's DPI the same way egui will (96 DPI = 1 point per pixel).
        ppp = self._guess_ppp()
        apps = mode in APP_MODES
        # Only "focus window" (and Ctrl+D) open the window list as a details table;
        # switching back from the app view returns to the layout last used.
        self.window_details = window_details
        if mode == "windows":
            self.window_details_last = window_details
        details_list = mode == "windows" and self.window_details
        previews = settings.get("user.thumbnail_switcher_previews") and not apps and not details_list
        pool = [Entry(w, previews, APP_ICON_PIXELS if apps else None) for w in windows]
        desktops, current = self._read_desktops()
        screens = screen_rects()
        for entry in pool:
            self._set_desktop(entry, desktops, current, previews)
            entry.screen_number = screen_number(entry.hwnd, screens)
        chip = None
        if chip_windows is not None:
            chip = Chip(chip_label, (w.id for w in chip_windows))
        launch_list = launcher_apps.LaunchList() if mode == "launcher" else None
        if mode == "apps" and self.apps_details is None:
            self.apps_details = bool(settings.get("user.thumbnail_switcher_apps_details"))
        apps_table = mode == "apps" and bool(self.apps_details)
        if apps:
            count = len(group_apps(pool)) + (len(launch_list.apps) if launch_list else 0)
            cols, width, height = choose_apps(count, work, ppp)
            if apps_table:
                # A row per app, under the column headings.
                cols = 1
                width = int(min(max(width, WINDOW_DETAILS_MIN_WIDTH * ppp), (work[2] - work[0]) * SCREEN_FILL))
                rows_h = (HEADER_HEIGHT + SEARCH_HEIGHT + COLUMN_HEADER_HEIGHT + 2 * PADDING + count * (DETAIL_ROW_HEIGHT + ROW_GAP)) * ppp
                height = int(min(max(rows_h, APPS_MIN_HEIGHT * ppp), (work[3] - work[1]) * SCREEN_FILL))
        elif previews:
            cols, width, height = choose_grid(len(pool), work, ppp)
        else:
            cols = 1
            width, height = choose_list(pool, work, ppp)
            if details_list:
                # Room for the columns, and their headings.
                width = int(min(max(width, WINDOW_DETAILS_MIN_WIDTH * ppp), (work[2] - work[0]) * SCREEN_FILL))
                height = int(min(height + COLUMN_HEADER_HEIGHT * ppp, (work[3] - work[1]) * SCREEN_FILL))
        if mode == "launcher":
            if self.launcher_details is None:
                self.launcher_details = bool(settings.get("user.thumbnail_switcher_launcher_details"))
            self.grid_cols = cols
            if self.launcher_details:
                cols = 1
        left = work[0] + ((work[2] - work[0]) - width) // 2
        top = work[1] + ((work[3] - work[1]) - height) // 2
        with self.lock:
            self.mode = mode
            self.launch_list = launch_list
            self.pool = pool
            self.desktops, self.current_desktop = desktops, current
            self.screen_count = len(screens)
            self.placement = None
            self.marked = []
            self.mark_anchor = None
            self.chip = chip
            self.query = ""
            self._refilter()
            self.previews = previews
            self.pointer_origin = None
            # Like Alt+Tab: start on the next window when the current one is first.
            first_is_current = bool(self.entries) and self.entries[0].hwnd == self.previous_foreground
            self.selected = 1 if first_is_current and len(self.entries) > 1 else 0
            self.cols = cols
            # The selection may start beyond the first screenful.
            self.reveal_selected = True
            self.target = (left, top, left + width, top + height)
            self.menu_restore = None
        self.showing = True
        self.had_focus = False
        if not self.events_registered:
            for event in WINDOW_EVENTS:
                ui.register(event, self._on_window_event)
            self.events_registered = True
        self.host.show()
        if self.hwnd is not None and not native.is_window(self.hwnd):
            self.hwnd = None
        if self.hwnd is not None:
            self._attach()
        if launch_list is not None:
            # Installed apps' icons arrive in the background.
            launcher_apps.load_icons(launch_list.apps, APP_ICON_PIXELS, self.refresh)
        # Changing tags rebuilds Talon's registry, which can take a while; do it last.
        self._update_tags()

    def hide(self):
        self.menu = None
        # Marks belong to one opening of the switcher.
        with self.lock:
            self.marked = []
        self.end_placement()
        if self.events_registered:
            for event in WINDOW_EVENTS:
                ui.unregister(event, self._on_window_event)
            self.events_registered = False
        self.showing = False
        self._clear_thumbnails()
        self.host.hide()
        self._update_tags()

    def refresh(self):
        """Redraw after a change. The window shows a frame late: what a refresh draws
        only appears with the next frame, so this asks for one more."""
        self.host.repaint(2)

    def _update_tags(self):
        """Tags for the switcher's voice commands; only set when they change, as each
        change rebuilds Talon's registry."""
        tags = []
        if self.showing:
            tags.append("user.thumbnail_switcher_showing")
            if self.menu is not None:
                tags.append("user.thumbnail_switcher_menu_open")
            if self.marked:
                tags.append("user.thumbnail_switcher_marked")
        if self.tag_context is not None and list(self.tag_context.tags) != tags:
            self.tag_context.tags = tags

    def cancel(self):
        """Close the switcher and give focus back to the window the user came from."""
        # Focus first: hiding the switcher while it is foreground would let Windows
        # activate whatever window is next in z-order.
        if self.previous_foreground is not None and native.is_window(self.previous_foreground):
            native.set_foreground(self.previous_foreground)
        self.hide()

    # --- searching ---

    def _refilter(self, keep_selection: bool = False):
        """Recompute `entries` from the chip and query; call with the lock held.

        A new search starts at the top. When windows come and go instead
        (`keep_selection`), the selection stays on its window, or on the tile that
        took the place of a window that went away.
        """
        selected = self.entries[self.selected] if keep_selection and 0 <= self.selected < len(self.entries) else None
        words = self.query.lower().split()
        if self.mode in APP_MODES:
            # The chip picks windows; the words match an app's name or any of its titles.
            groups = group_apps([e for e in self.pool if matches(e, self.chip, [])])
            # Apps with a window on this desktop first; each part in recency order.
            groups.sort(key=lambda g: all(w.away for w in g.windows))
            self.entries = [g for g in groups if all(word in g.search_text for word in words)]
            if self.mode == "apps" and self.apps_details:
                self._read_spoken_forms()
                if self.apps_sort:
                    self.entries = sorted(self.entries, key=self._sort_key(self.apps_sort), reverse=self.apps_sort_reverse)
            if self.mode == "launcher" and self.launch_list is not None:
                # Running apps first (most recent first), each matched to its installed
                # app; then the other installed apps, alphabetically. A chip (app:,
                # desk:, screen:) is about windows: only running apps then.
                running = set()
                for group in self.entries:
                    group.launch = self.launch_list.match(group.hwnd, group.app_name)
                    if group.launch is not None:
                        running.add(group.launch.app_id.lower())
                self.running_count = len(self.entries)
                installed = []
                if self.chip is None:
                    installed = [
                        app
                        for app in self.launch_list.apps
                        if app.app_id.lower() not in running and all(word in app.search_text for word in words)
                    ]
                self._read_spoken_forms()
                if self.launcher_sort:
                    # Sorted within each section; running apps stay first.
                    key = self._sort_key(self.launcher_sort)
                    self.entries = sorted(self.entries, key=key, reverse=self.launcher_sort_reverse)
                    installed = sorted(installed, key=key, reverse=self.launcher_sort_reverse)
                self.entries += installed
        else:
            self.entries = [e for e in self.pool if matches(e, self.chip, words)]
            if self.chip is None and not words:
                # Unfiltered: this desktop's windows first, each part in recency order.
                self.entries.sort(key=lambda e: bool(e.away))
            if self.mode == "windows" and self.window_details:
                self._read_spoken_forms()
                if self.window_sort:
                    self.entries = sorted(self.entries, key=self._sort_key(self.window_sort), reverse=self.window_sort_reverse)
        index = next((i for i, e in enumerate(self.entries) if selected and e.hwnd == selected.hwnd), None)
        if not keep_selection:
            self.selected = 0
            self.scroll = 0.0
            self.reveal_selected = True
        elif index is not None:
            self.selected = index
        else:
            self.selected = min(self.selected, max(len(self.entries) - 1, 0))

    def set_query(self, query: str):
        with self.lock:
            if query == self.query:
                return
            self.query = query
            self._refilter()
        self.refresh()

    def set_chip(self, chip: Chip | None):
        with self.lock:
            self.chip = chip
            self._refilter()
        self.refresh()

    def set_app(self, name: str):
        """Lock the search to the app called `name` (by voice), or the closest match."""
        with self.lock:
            pool = self.pool
        chip = app_chip(pool, name)
        if chip is None:
            found = resolve_app([(e.app_name, e.exe_name) for e in pool], name)
            chip = app_chip(pool, found) if found else None
        if chip is not None:
            self.set_chip(chip)

    def lock_tag(self):
        """Tab: turn "app:<text>" or "desk:<n>" in the search field into a chip."""
        with self.lock:
            query = self.query
            pool = self.pool
        if query.lower().startswith(DESK_TAG):
            number = query[len(DESK_TAG):].strip()
            if number.isdigit():
                self.set_desk(int(number), clear_query=True)
            return
        if query.lower().startswith(SCREEN_TAG):
            number = query[len(SCREEN_TAG):].strip()
            if number.isdigit():
                self.set_screen(int(number), clear_query=True)
            return
        if not query.lower().startswith(APP_TAG):
            return
        name = resolve_app([(e.app_name, e.exe_name) for e in pool], query[len(APP_TAG):])
        chip = app_chip(pool, name) if name else None
        if chip is None:
            return
        with self.lock:
            self.chip = chip
            self.query = ""
            self._refilter()
        self.refresh()

    def set_desk(self, number: int, clear_query: bool = False):
        """Filter to the windows on virtual desktop `number` (1-based)."""
        with self.lock:
            desktop = next((d for d in self.desktops if d.number == number), None)
            if desktop is None:
                return
            self.chip = Chip(desktop.label(), tag=DESK_TAG, desktop=desktop.guid.key())
            if clear_query:
                self.query = ""
            self._refilter()
        self.refresh()

    def set_screen(self, number: int, clear_query: bool = False):
        """Filter to the windows on screen `number` (1-based, like the screen commands)."""
        with self.lock:
            if not 0 < number <= self.screen_count:
                return
            self.chip = Chip(f"Screen {number}", tag=SCREEN_TAG, screen=number)
            if clear_query:
                self.query = ""
            self._refilter()
        self.refresh()

    def backspace(self, word: bool):
        """Delete the last character (or word); in an empty field, remove the chip."""
        with self.lock:
            query, chip = self.query, self.chip
        if query:
            if word:
                trimmed = query.rstrip()
                self.set_query(trimmed[: len(trimmed) - len(trimmed.split()[-1])] if trimmed else "")
            else:
                self.set_query(query[:-1])
        elif chip is not None:
            self.set_chip(None)

    def escape(self):
        """Close the menu, else leave placement, else clear the marks, else clear the
        search text, else close the switcher."""
        if self.menu is not None:
            self.close_menu()
        elif self.placement is not None:
            self.end_placement()
        elif self.marked:
            self.clear_marks()
        elif self.query:
            self.set_query("")
        else:
            self.cancel()

    def move_selection(self, step: int, mark: bool = False):
        """Move the selection; with `mark` (Shift), marking the tiles it passes over."""
        with self.lock:
            if self.entries:
                start = self.selected
                self.selected = max(0, min(self.selected + step, len(self.entries) - 1))
                self.reveal_selected = True
                if mark:
                    self._set_marks(self.entries[min(start, self.selected) : max(start, self.selected) + 1], True)
        self.refresh()

    def set_launcher_details(self, on: bool | None = None):
        """Show the launcher as a details table (True), an icon grid (False), or switch
        (None). The choice holds for the session."""
        with self.lock:
            details = (not self.launcher_details) if on is None else on
            self.launcher_details = details
            if self.mode == "launcher":
                self.cols = 1 if details else max(self.grid_cols, 1)
                self.reveal_selected = True
        self.refresh()

    def switch_view(self, mode: str | None = None):
        """From the window view to the app view or back (or to `mode`), without the
        search, filters or marks; each view opens in the layout it last had."""
        mode = mode or ("apps" if self.mode == "windows" else "windows")
        if mode == "apps":
            self.show(all_windows() or [], mode="apps")
        else:
            self.show(all_windows() or [], mode="windows", window_details=self.window_details_last)

    def set_apps_details(self, on: bool):
        """The running applications as a details table (True) or icons; reopens, as the
        window's size differs, keeping the search."""
        with self.lock:
            chip, query = self.chip, self.query
        self.apps_details = bool(on)
        self.show(all_windows() or [], mode="apps")
        with self.lock:
            self.chip = chip
            self.query = query
            self._refilter()
        self.refresh()

    def show_window_details(self, on: bool):
        """The window list as a details table (a row per window) or as before; reopens,
        as the window's size and live previews differ."""
        with self.lock:
            chip, query = self.chip, self.query
        self.show(all_windows() or [], mode="windows", window_details=on)
        with self.lock:
            self.chip = chip
            self.query = query
            self._refilter()
        self.refresh()

    def sort_launcher(self, column: str | None):
        """Sort the launcher by a column (again: the other way round); None: the default
        order."""
        with self.lock:
            if column not in SORTABLE:
                column = None
            if self.mode == "apps" and self.apps_details:
                if column is not None and column == self.apps_sort:
                    self.apps_sort_reverse = not self.apps_sort_reverse
                else:
                    self.apps_sort, self.apps_sort_reverse = column, False
                self._refilter(keep_selection=True)
                self.reveal_selected = True
                self.refresh()
                return
            if self.mode == "windows" and self.window_details:
                if column is not None and column == self.window_sort:
                    self.window_sort_reverse = not self.window_sort_reverse
                else:
                    self.window_sort, self.window_sort_reverse = column, False
                self._refilter(keep_selection=True)
                self.reveal_selected = True
                self.refresh()
                return
            if column is not None and column == self.launcher_sort:
                self.launcher_sort_reverse = not self.launcher_sort_reverse
            else:
                self.launcher_sort, self.launcher_sort_reverse = column, False
            self._refilter(keep_selection=True)
            self.reveal_selected = True
        self.refresh()

    def _sort_key(self, column: str):
        def key(entry):
            windows = getattr(entry, "windows", [])
            if isinstance(entry, Entry):
                # A window row.
                if column == "name":
                    return (entry.app_name.lower(), entry.title.lower())
                if column == "state":
                    return (window_state(entry), entry.title.lower())
                if column == "desktop":
                    return (entry.desktop_number or 99, entry.title.lower())
                if column == "screen":
                    return (entry.screen_number or 99, entry.title.lower())
                if column == "spoken":
                    return (self._spoken_forms(entry) or ["~"])[0].lower()
                return entry.title.lower()
            if column == "running":
                return (-len(windows), entry.title.lower())
            if column == "spoken":
                return (self._spoken_forms(entry) or ["~"])[0].lower()
            if column == "desktop":
                return (getattr(entry, "desktop_numbers", None) or [99], entry.title.lower())
            if column == "screen":
                return (getattr(entry, "screen_numbers", None) or [99], entry.title.lower())
            return entry.title.lower()

        return key

    def _read_spoken_forms(self):
        """The spoken forms to show: the running list's for running apps, the launch
        list's for installed ones. Call with the lock held."""
        running, launch = {}, {}
        try:
            for spoken, value in (registry.lists.get("user.running") or [{}])[-1].items():
                running.setdefault(str(value).lower(), []).append(spoken)
            for spoken, value in (registry.lists.get("user.launch") or [{}])[-1].items():
                launch.setdefault(str(value).lower(), []).append(spoken)
        except Exception as e:
            print(f"thumbnail_switcher: reading spoken forms failed: {e!r}")
        # Shortest first: what you'd actually say.
        self.spoken_running = {k: sorted(v, key=len) for k, v in running.items()}
        self.spoken_launch = {k: sorted(v, key=len) for k, v in launch.items()}

    def _spoken_forms(self, entry) -> list[str]:
        if isinstance(entry, Entry):
            return self.spoken_running.get(entry.app_name.lower(), [])
        if getattr(entry, "windows", None):
            forms = self.spoken_running.get(entry.app_name.lower())
            if forms:
                return forms
        return self.spoken_launch.get(launch_id(entry).lower(), [])

    def jump(self, letter: str):
        """Launcher: select the first installed app starting with `letter` ("#" for digits
        and symbols), or the next letter that has one, and scroll it to the top. Works
        within the search results."""
        letter = letter.upper()[:1] or "#"
        with self.lock:
            if self.mode != "launcher":
                return
            wanted = INDEX_LETTERS.index(letter if letter in INDEX_LETTERS else "#")
            letters = launcher_letters(self.entries, self.running_count)
            target = next((first for first, l in letters.items() if INDEX_LETTERS.index(l) >= wanted), None)
            if target is None:
                return
            self.selected = target
            self.scroll_to = target
        self.refresh()

    def move_row(self, rows: int, mark: bool = False):
        """Move the selection `rows` rows up or down, to the nearest tile in that row: the
        launcher's sections start new rows, so a fixed step would land a column off."""
        with self.lock:
            layout = self.layout if len(self.layout) == len(self.entries) else []
            if layout:
                current = min(self.selected, len(layout) - 1)
                col, row, _ = layout[current]
                last_row = layout[-1][1]
                target_row = max(0, min(row + rows, last_row))
                in_row = [i for i, (c, r, _) in enumerate(layout) if r == target_row]
                if in_row:
                    target = min(in_row, key=lambda i: abs(layout[i][0] - col))
                    start = self.selected
                    self.selected = target
                    self.reveal_selected = True
                    if mark:
                        self._set_marks(self.entries[min(start, target) : max(start, target) + 1], True)
        if not layout:
            self.move_selection(rows * max(self.cols, 1), mark=mark)
            return
        self.refresh()

    def move_to_end(self, end: bool):
        """Home/End: the first or last tile."""
        with self.lock:
            if self.entries:
                self.selected = len(self.entries) - 1 if end else 0
                self.reveal_selected = True
        self.refresh()

    def select(self, index: int):
        """Focus the window on tile `index` (1-based) and close the switcher; while a
        menu is open, pick its item `index` instead; while placing, put the window in
        the current slot."""
        if self.menu is not None:
            self.pick_menu_item(index)
            return
        if self.placement is not None:
            self.place(index)
            return
        entries = self.entries_at([index])
        if entries and isinstance(entries[0], launcher_apps.InstalledApp):
            self.launch(index)
            return
        if entries and isinstance(entries[0], AppGroup):
            entries = [entries[0].best_window()]
        if entries:
            self._activate(entries)

    def launch(self, index: int):
        """Launch the app on tile `index`: an installed app, or another instance of a
        running one (its window if it only runs once). The switcher closes; the new
        window takes the focus."""
        entries = self.entries_at([index])
        if not entries:
            return
        entry = entries[0]
        installed = entry if isinstance(entry, launcher_apps.InstalledApp) else getattr(entry, "launch", None)
        try:
            if installed is not None:
                launcher_apps.launch(app_id=installed.app_id)
            elif isinstance(entry, AppGroup):
                # Running, but not in the launch list (Talon, a portable app): its
                # executable.
                launcher_apps.launch(path=app_identity.resolve(entry.hwnd, entry.app_name).exe_path)
            else:
                return
        except OSError as e:
            app.notify("App launcher", f"Couldn't launch {entry.app_name}: {e}")
            return
        self.hide()

    def show_app_windows(self, index: int):
        """From the apps view: the window switcher, filtered to that app (Cmd+Tab, Down)."""
        entries = self.entries_at([index])
        if not entries or not isinstance(entries[0], AppGroup):
            return
        group = entries[0]
        windows = [w.window for w in group.windows]
        self.show(all_windows(), windows, group.app_name)

    def entries_at(self, indices: list[int]) -> list[Entry]:
        """The entries with these tile numbers (1-based, as shown), skipping bad ones."""
        with self.lock:
            return [self.entries[i - 1] for i in indices if 0 < i <= len(self.entries)]


    # --- managing windows by number ---
    # All of these leave the switcher open, focused and on the same tile.


    # --- marking several windows ---
    # Marks pick the windows the marked-window commands, the header's buttons, the
    # marked windows' menu and Delete act on; focusing still takes one window.

















    # --- the right-click menu ---


    # --- placing windows into a layout, slot by slot ---


    # --- virtual desktops ---


    # --- following window changes ---







    # --- native window and DWM thumbnails ---






    # --- drawing ---

















    def shutdown(self):
        """Stop for good (hot reload): hide, stop the timer, close the window."""
        self.hide()
        self.overlay.close()
        self.grid_overlay.close()
        cron.cancel(self.tick_job)
        self.host.close()
