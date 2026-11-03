"""Prototype: an app switcher that shows live DWM thumbnails in a talon.egui window.

Two optional commands (enabled by tags, see thumbnail_switcher_enable.talon):
  * every open or minimized window Talon sees
  * the windows of one running application (from the community app switcher's
    user.running_applications list)

The egui window lays out one tile per window and reserves a rectangle in each tile;
DWM composites the live thumbnail of the source window onto that rectangle. Minimized
windows have no thumbnail content, so their tile shows the app's icon instead. With the
user.thumbnail_switcher_previews setting off, it shows a compact list instead: one row
per window with a small icon, the window title and the app name.

Both views scroll (mouse wheel, or by moving the selection) when there are more windows
than fit on the screen.

A search field above the tiles filters them by window title and app name as you type.
Like Fluent Search's search tags, an app filter can be locked in as a pill in front of
the text: the per-app commands open with one, typing "app:<name>" and pressing Tab adds
one, and Backspace in the empty field removes it again.

Clicking a tile, saying its number, or moving the selection with the arrow keys and
pressing Enter focuses that window; Escape clears the search, then closes the switcher.
Windows can also be managed by number while it shows (see
thumbnail_switcher_showing.talon): closed, minimized, restored, maximized, snapped to a
community snap position or another screen, or laid out side by side. Delete closes the
selected window. The switcher stays open and keeps focus for all of these, and follows
windows that are closed, minimized, restored, retitled, moved or opened meanwhile,
whether through it or elsewhere.

Windows on every virtual desktop are listed; with more than one desktop, each tile
shows which desktop it is on, windows can be moved between desktops, and "desk:<n>" +
Tab filters to one desktop. With more than one screen, tiles also show their screen,
numbered like community's screen commands, and "screen:<n>" + Tab filters to one.

"app icons" opens the same switcher with one large icon per application instead, like
Cmd+Tab: choosing an app focuses its most recent window, on the current desktop if it
has one there; Down (or "windows <number>") shows that app's windows instead.

Right-clicking a tile (or Shift+F10, or "menu <number>") opens a menu of the same
actions: focus, close, minimize or restore, maximize, snap, move to another desktop,
and filter to the window's app.

"layout <half | third | ...>" fills a layout one slot at a time: the header names the
slot, a mini-map shows it, and a frame on screen outlines it; saying a window's number
(or Enter, or a click) puts that window there and moves on to the next slot.
"""

import ctypes
import math
import re
import os
import sys
import threading
import time
from typing import Any

import egui
from talon import Context, Module, actions, app, cron, registry, settings, ui
from talon.egui import Window

from . import dwm_thumbnails as dwm
from ..windows import virtual_desktops as vd
from ..windows import app_identity, jump_lists, shell_apps, window_filter
from . import launcher_apps, window_icons
from ..windows.com_thread import on_com_thread

window_model_id = app_identity.window_model_id


mod = Module()
mod.tag("thumbnail_switcher_all", desc="Enables the command showing thumbnails of every window")
mod.tag("thumbnail_switcher_app", desc="Enables the command showing thumbnails for one application")
mod.tag("thumbnail_switcher_icons", desc="Enables the command showing one icon per application")
mod.tag("thumbnail_switcher_launcher", desc="Enables the command showing the app launcher")
mod.tag("thumbnail_switcher_showing", desc="The thumbnail switcher is showing")
mod.tag("thumbnail_switcher_menu_open", desc="A right-click menu is open in the thumbnail switcher")
mod.tag("thumbnail_switcher_marked", desc="Windows are marked in the thumbnail switcher (the marked bar's commands)")
mod.list("thumbnail_switcher_layouts", desc="Arrangements for laying out several windows")
mod.setting(
    "thumbnail_switcher_launcher_details",
    type=bool,
    default=False,
    desc="Open the app launcher as a details table rather than an icon grid",
)
mod.setting(
    "thumbnail_switcher_apps_details",
    type=bool,
    default=False,
    desc="Open the running applications view as a details table rather than icons",
)
mod.list("thumbnail_switcher_columns", desc="Columns of the app launcher's details view")
mod.setting(
    "thumbnail_switcher_previews",
    type=bool,
    default=False,
    desc="Show live window thumbnails in the switcher; when off, show a compact list",
)

ctx = Context()
# The spoken forms and arrangements of community's window_split_positions list (from
# the experimental, currently disabled, window_layout.py); values are keys of
# window_snap.py's snap positions.
LAYOUTS = {
    "HALVES": ["LEFT", "RIGHT"],
    "THIRDS": ["LEFT_THIRD", "CENTER_THIRD", "RIGHT_THIRD"],
    "CLOCK": ["LEFT", "TOP_RIGHT", "BOTTOM_RIGHT"],
    "COUNTERCLOCK": ["RIGHT", "TOP_LEFT", "BOTTOM_LEFT"],
    "GRID": ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
    "BIG_GRID": [
        "TOP_LEFT_THIRD",
        "TOP_CENTER_THIRD",
        "TOP_RIGHT_THIRD",
        "BOTTOM_LEFT_THIRD",
        "BOTTOM_CENTER_THIRD",
        "BOTTOM_RIGHT_THIRD",
    ],
}
ctx.lists["user.thumbnail_switcher_columns"] = {
    "application": "name",
    "name": "name",
    "active windows": "running",
    "active": "running",
    "running": "running",
    "windows": "running",
    "spoken": "spoken",
    "spoken form": "spoken",
    "virtual desktop": "desktop",
    "desktop": "desktop",
    "desktops": "desktop",
    "screen": "screen",
    "window": "title",
    "title": "title",
    "state": "state",
}
ctx.lists["user.thumbnail_switcher_layouts"] = {
    "half": "HALVES",
    "third": "THIRDS",
    "clock": "CLOCK",
    "counterclock": "COUNTERCLOCK",
    "grid": "GRID",
    "big grid": "BIG_GRID",
}
# How long to wait before checking which windows actually closed: some ask to save.
CLOSE_CHECKS = ("300ms", "1500ms")
# Talon window events that can change what the switcher shows.
WINDOW_EVENTS = ("win_open", "win_close", "win_show", "win_hide", "win_title", "win_move", "win_resize")
# Polling fallback for changes Talon has no event for (minimizing), in ticks.
SYNC_EVERY_TICKS = 10
# Commands like maximize briefly activate the window they act on; for this long
# afterwards the switcher takes focus back instead of closing.
HOLD_FOCUS_SECONDS = 1.0


@mod.capture(rule="<number_small> ([and] <number_small>)*")
def thumbnail_switcher_numbers(m) -> list[int]:
    """One or more tile numbers: "three", "one and four", "two five"."""
    return m.number_small_list

WINDOW_TITLE = "Talon thumbnail switcher"
TICK_MS = 50
GUARD_EVERY_TICKS = 5

# Layout, in egui points
HEADER_HEIGHT = 28.0
SEARCH_HEIGHT = 40.0  # the search field and the space around it, below the header
PADDING = 8.0
LABEL_HEIGHT = 22.0
# Tile shape used to choose the grid, in physical pixels
TILE_ASPECT = 16 / 10
MAX_TILE_WIDTH_FRACTION = 1 / 3  # of the work area width
# Tiles never get narrower than this; with more windows, the grid scrolls instead.
MIN_TILE_WIDTH = 240.0  # egui points
SCREEN_FILL = 0.9  # the switcher uses at most this much of the work area
# List view (previews off), in egui points
ROW_HEIGHT = 36.0
ROW_GAP = 4.0
ROW_ICON = 24.0
NUMBER_WIDTH = 30.0
LIST_MIN_WIDTH = 640.0
LIST_MAX_WIDTH_FRACTION = 0.55  # of the work area width
LIST_ICON_PIXELS = 64
SCROLLBAR_WIDTH = 4.0

BACKGROUND = egui.Color32.from_rgb(24, 24, 28)
TILE = egui.Color32.from_rgb(40, 40, 46)
TILE_HOVER = egui.Color32.from_rgb(60, 70, 95)
BORDER = egui.Color32.from_rgb(90, 90, 100)
SELECTED = egui.Color32.from_rgb(70, 150, 255)
SELECTED_WIDTH = 3.0
WHITE = egui.Color32.from_rgb(255, 255, 255)
ICON_POINTS = 96.0
TEXT = egui.Color32.from_rgb(235, 235, 235)
DIM_TEXT = egui.Color32.from_rgb(150, 150, 160)
CHIP = egui.Color32.from_rgb(45, 85, 150)
CURRENT_DESKTOP = egui.Color32.from_rgb(45, 110, 80)
APP_TAG = "app:"
DESK_TAG = "desk:"
SCREEN_TAG = "screen:"
SCREEN_BADGE = egui.Color32.from_rgb(105, 80, 140)
# Marked tiles (multi-select): their outline and check, and their fill.
MARKED = egui.Color32.from_rgb(230, 160, 40)
MARKED_FILL = egui.Color32.from_rgb(66, 56, 38)
MARK_BAR_FONT = 13.0
CLOSE_BUTTON = 22.0  # the header's close button, egui points
CLOSE_HOVER = egui.Color32.from_rgb(196, 43, 28)
TILE_CLOSE = 18.0  # each tile's close button, egui points
# Apps view: square cells with a large icon, in egui points.
APP_CELL = 150.0
APP_ICON = 80.0
APP_ICON_PIXELS = 128
APP_MAX_COLUMNS = 8
APPS_MIN_WIDTH = 560.0
# Tall enough for an app's full right-click menu (twelve items and three separators)
# under the header and search field, however few apps there are.
APPS_MIN_HEIGHT = 580.0
WINDOW_DETAILS_MIN_WIDTH = 1100.0
# Views with a tile per application: the apps strip, and the launcher (running apps,
# then every installed app).
APP_MODES = ("apps", "launcher")
# The launcher's section headings ("Running", "Apps"), egui points.
SECTION_HEIGHT = 28.0
RUNNING_DOT = egui.Color32.from_rgb(80, 200, 120)
# The launcher's A-Z index along the right edge, egui points; "#" is digits and symbols.
INDEX_WIDTH = 22.0
INDEX_LETTERS = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Rows on one page of a jump list menu.
JUMP_PAGE_ROWS = 14
# The launcher's details view: rows, the sticky column headings, and the columns as
# (key, heading, width in points; 0: takes the rest). "screen" only with 2+ screens.
DETAIL_ROW_HEIGHT = 30.0
COLUMN_HEADER_HEIGHT = 26.0
DETAIL_COLUMNS = [
    ("number", "#", 38.0),
    ("icon", "", 30.0),
    ("name", "Application", 0.0),
    ("spoken", "Spoken form", 260.0),
    ("running", "Active Windows", 130.0),
    ("desktop", "Virtual Desktop", 140.0),
    ("screen", "Screens", 90.0),
]
# The window list's details view ("focus window"): a row per window.
WINDOW_DETAIL_COLUMNS = [
    ("number", "#", 38.0),
    ("icon", "", 30.0),
    ("title", "Window", 0.0),
    ("name", "Application", 220.0),
    ("spoken", "Spoken form", 200.0),
    ("state", "State", 110.0),
    ("desktop", "Virtual Desktop", 140.0),
    ("screen", "Screen", 90.0),
]
SORTABLE = {"name", "running", "spoken", "desktop", "screen", "title", "state"}
# Jump list pages are wider (titles are long), with icon buttons on their rows.
JUMP_MENU_WIDTH = 360.0
MENU_BUTTON = 20.0
MENU_BUTTON_TIPS = {"pin": "Pin to this list", "unpin": "Unpin from this list", "remove": "Remove from this list"}
# Sized like the Windows 11 Start menu's context menu: rows 36 points, headings in
# small grey text, a gutter with the voice number, then an icon column and the label.
MENU_WIDTH = 290.0  # egui points
MENU_ITEM_HEIGHT = 36.0
MENU_SEPARATOR_HEIGHT = 9.0
MENU_PADDING = 4.0
MENU_ICON = 16.0
MENU_LABEL_X = 52.0  # from the row's left edge
MENU_BACKGROUND = egui.Color32.from_rgb(44, 44, 46)
MENU_BORDER = egui.Color32.from_rgb(72, 72, 78)
MENU_HOVER = egui.Color32.from_rgb(64, 64, 70)
# The snap positions the menu offers, as community window_snap.py keys.
MENU_SNAPS = ["LEFT", "RIGHT", "TOP", "BOTTOM", "TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT", "FULL"]
OVERLAY_TITLE = "Talon thumbnail placement"
GRID_OVERLAY_TITLE = "Talon thumbnail placement grid"
OVERLAY_THICKNESS = 10  # physical pixels
MINIMAP_WIDTH = 64.0  # egui points
# egui.Key values don't compare equal to each other, but their reprs do.
KEY_NAMES = {
    repr(getattr(egui.Key, name)): name
    for name in (
        "ArrowUp",
        "ArrowDown",
        "ArrowLeft",
        "ArrowRight",
        "Backspace",
        "Tab",
        "Enter",
        "Escape",
        "Delete",
        "F10",
        "Space",
        *"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "PageUp",
        "PageDown",
        "Home",
        "End",
    )
}


class Entry:
    def __init__(self, window: ui.Window, previews: bool, icon_size: int | None = None):
        self.window = window
        self.hwnd = window.id
        self.title = window.title
        try:
            self.app_name = window.app.name
        except Exception:
            self.app_name = ""
        try:
            self.exe_name = os.path.basename(window.app.exe)
        except Exception:
            self.exe_name = ""
        # What the search words are matched against.
        self.search_text = f"{self.title} {self.app_name} {self.exe_name}".lower()
        self.minimized = dwm.is_minimized(self.hwnd)
        # The virtual desktop it's on: GUID, its key (bytes), its number (1-based), and
        # whether that is another desktop than the current one; set by the switcher.
        self.desktop: vd.GUID | None = None
        self.desktop_key: bytes | None = None
        self.desktop_number: int | None = None
        self.away = False
        # The screen it's on (or restores to), numbered like ui.screens(); set by the
        # switcher.
        self.screen_number: int | None = None
        # Name and group it like the taskbar does (shared with the app switcher), but
        # keep Talon's name for searching ("edge" still finds Slack's window).
        identity = app_identity.resolve(self.hwnd, self.app_name)
        self.talon_app_name = self.app_name
        self.app_name = identity.name
        self.model_id = identity.model_id
        # Hosted under another app's id, like a PWA in Edge: the window has the right
        # icon, the executable doesn't.
        self.hosted = identity.hosted
        # The .msc an MMC console opened: its icon is the console's (see _find_icon).
        self.document = identity.icon_source
        # Talon can attribute a window to another process (a console to cmd or
        # conhost); the owning process is what groups windows into apps.
        self.process = identity.process
        self.key = identity.key
        self.search_text = self._search_text()
        self.icon: window_icons.Icon | None = None
        if icon_size:
            self.icon = self._find_icon(window, icon_size)
        elif not previews:
            self.icon = self._find_icon(window, LIST_ICON_PIXELS)
        elif self.minimized:
            self.icon = self._find_icon(window, window_icons.ICON_SIZE)

    @property
    def iconic(self) -> bool:
        """Shown with its icon: DWM has no useful thumbnail of it."""
        return self.minimized or self.away

    def set_title(self, title: str):
        self.title = title
        self.search_text = self._search_text()

    def _search_text(self) -> str:
        names = {self.app_name, getattr(self, "talon_app_name", self.app_name)}
        return " ".join([self.title, *names, self.exe_name]).lower()

    def app_label(self) -> str:
        return f"{self.app_name} (minimized)" if self.minimized else self.app_name

    def state_label(self) -> str:
        if self.minimized:
            return f"{self.app_name} (minimized)"
        if self.away and self.desktop_number:
            return f"{self.app_name} (desktop {self.desktop_number})"
        return self.app_name

    def _find_icon(self, window: ui.Window, size: int) -> "window_icons.Icon | None":
        try:
            exe = window.app.exe
        except Exception:
            exe = None
        model_id = getattr(self, "model_id", None)
        try:
            # Applets in rundll32/dllhost: their window's icon at any size (the taskbar's).
            command_line_host = getattr(self, "process", "") in app_identity.COMMAND_LINE_HOSTS
            return window_icons.window_icon(
                self.hwnd,
                exe,
                model_id,
                size,
                own_first=getattr(self, "hosted", False),
                document=getattr(self, "document", None),
                own_min=1 if command_line_host else 48,
            )
        except Exception as e:
            print(f"thumbnail_switcher: icon for {self.title!r} failed: {e!r}")
            return None


class Chip:
    """A locked filter shown as a pill in front of the search text: an app's windows,
    or (with `desktop`) the windows on one virtual desktop."""

    def __init__(
        self,
        label: str,
        hwnds=(),
        tag: str = APP_TAG,
        desktop: bytes | None = None,
        screen: int | None = None,
    ):
        self.label = label
        self.hwnds = frozenset(hwnds)
        self.tag = tag
        self.desktop = desktop
        self.screen = screen


def matches(entry: Entry, chip: Chip | None, words: list[str]) -> bool:
    if chip is not None:
        if chip.desktop is not None:
            if entry.desktop_key != chip.desktop:
                return False
        elif chip.screen is not None:
            if entry.screen_number != chip.screen:
                return False
        elif entry.hwnd not in chip.hwnds:
            return False
    return all(word in entry.search_text for word in words)


def screen_rects() -> list[tuple[int, int, int, int]]:
    """The screens as (left, top, right, bottom), in the order community's screen
    commands number them (ui.screens(), from 1)."""
    rects = []
    for screen in ui.screens():
        r = screen.rect
        rects.append((int(r.x), int(r.y), int(r.x + r.width), int(r.y + r.height)))
    return rects


def screen_work_rects() -> list[tuple[int, int, int, int]]:
    """The screens' usable areas (without the taskbar), in screen_rects() order."""
    rects = []
    for screen in ui.screens():
        r = screen.visible_rect
        rects.append((int(r.x), int(r.y), int(r.x + r.width), int(r.y + r.height)))
    return rects


def screen_number(hwnd: int, screens: list[tuple[int, int, int, int]]) -> int | None:
    """The screen holding most of the window (or of where a minimized one restores to)."""
    rect = dwm.placed_rect(hwnd)
    best, best_area = None, 0
    for number, screen in enumerate(screens, 1):
        overlap = dwm.intersect(rect, screen)
        area = (overlap[2] - overlap[0]) * (overlap[3] - overlap[1]) if overlap else 0
        if area > best_area:
            best, best_area = number, area
    return best


class AppGroup:
    """One application in the apps view: its windows, most recently used first.

    It stands in for an entry where the switcher expects one; its window-ish fields
    are those of its most recent window.
    """

    def __init__(self, windows: list[Entry]):
        self.windows = windows
        first = windows[0]
        self.hwnd = first.hwnd
        self.window = first.window
        # The name most of its windows carry: Talon can name a console cmd or conhost.
        names = [w.app_name for w in windows if w.app_name]
        self.app_name = max(set(names), key=names.count) if names else ""
        self.title = self.app_name or first.title
        self.exe_name = first.exe_name
        self.icon = next((w.icon for w in windows if w.icon is not None), None)
        self.search_text = " ".join([first.app_name, first.exe_name] + [w.title for w in windows]).lower()
        self.minimized = all(w.minimized for w in windows)
        self.desktop = first.desktop
        self.desktop_key = first.desktop_key
        # No single desktop: the badges list them all.
        self.desktop_number = None
        self.desktop_numbers = sorted({w.desktop_number for w in windows if w.desktop_number})
        self.screen_number = None
        self.screen_numbers = sorted({w.screen_number for w in windows if w.screen_number})
        self.away = all(w.away for w in windows)
        self.iconic = True

    def best_window(self) -> Entry:
        """Its most recent window on the current desktop, else its most recent one."""
        return next((w for w in self.windows if not w.away), self.windows[0])

    def state_label(self) -> str:
        return self.title


def app_key(entry: Entry) -> tuple[str, str]:
    """What makes windows one application, like one taskbar button (see
    app_identity.AppIdentity.key)."""
    return entry.key


def group_apps(entries: list[Entry]) -> list[AppGroup]:
    """Group windows by app, in order of each app's most recent window."""
    groups: dict[tuple[str, str], list[Entry]] = {}
    for entry in entries:
        groups.setdefault(app_key(entry), []).append(entry)
    return [AppGroup(windows) for windows in groups.values()]


def index_letter(name: str) -> str:
    """The A-Z index letter of an app name; "#" for digits and symbols."""
    letter = name[:1].upper()
    return letter if "A" <= letter <= "Z" else "#"


def launcher_sections(entries: list, running: int) -> list[tuple[int, str]]:
    """The launcher's sections as (first tile, heading): running apps, installed apps."""
    sections = []
    if running:
        sections.append((0, f"Running ({running})"))
    if len(entries) > running:
        sections.append((running, f"Apps ({len(entries) - running})"))
    return sections


def launcher_letters(entries: list, running: int) -> dict[int, str]:
    """The first installed app of each index letter: tile -> letter. They carry a
    letter marker and are where jumps land."""
    letters, previous = {}, None
    for i in range(running, len(entries)):
        letter = index_letter(entries[i].title)
        if letter != previous:
            letters[i] = previous = letter
    return letters


def tile_layout(count: int, cols: int, sections: list) -> list[tuple[int, int, int]]:
    """Each tile's (column, row, section headings above it). Each section starts on a
    new row under its heading; without sections, tiles simply wrap."""
    starts = {first: n for n, (first, _heading) in enumerate(sections)}
    layout, row, col, section = [], 0, 0, -1
    for i in range(count):
        if i in starts:
            if col > 0:
                row += 1
            col, section = 0, starts[i]
        elif col == cols:
            row, col = row + 1, 0
        layout.append((col, row, section + 1))
        col += 1
    return layout


def launch_id(entry) -> str:
    """The app's launch list id (Apps folder id), if it has one."""
    installed = entry if isinstance(entry, launcher_apps.InstalledApp) else getattr(entry, "launch", None)
    return installed.app_id if installed is not None else ""


def detail_columns(width: float, screens: bool, definition=DETAIL_COLUMNS) -> list[tuple[str, str, float, float]]:
    """The details view's columns as (key, heading, x, width), x from the row's start."""
    columns = [c for c in definition if c[0] != "screen" or screens]
    rest = max(width - sum(w for _k, _h, w in columns), 120.0)
    out, x = [], 0.0
    for key, heading, w in columns:
        w = w or rest
        out.append((key, heading, x, w))
        x += w
    return out


def window_state(entry: "Entry") -> str:
    """A window row's State column."""
    if entry.minimized:
        return "Minimized"
    return "Maximized" if dwm.is_maximized(entry.hwnd) else "Normal"


def tile_hwnds(entry: "Entry | AppGroup") -> list[int]:
    """The windows a tile stands for: its window, or all of an app's."""
    return [w.hwnd for w in getattr(entry, "windows", [entry])]


# Whether a window belongs in the switcher, on this desktop or another one: the rule
# the app switcher's running list uses too.
is_switchable = window_filter.is_switchable


class Menu:
    """The right-click menu of one window, or with `marked` of the marked windows
    (`hwnd` None); `page` is "main" or a submenu's name."""

    def __init__(
        self, hwnd: int | None, pos: "egui.Pos2 | None", marked: bool = False, page: str = "main", dropdown: bool = False
    ):
        self.hwnd = hwnd
        # A marked bar button's dropdown: just that page's items, under the button, no
        # "< Back"; Left/Right go to the neighbouring button's dropdown.
        self.dropdown = dropdown
        # Where it opens, in points; None: at the window's tile (keyboard, voice).
        self.pos = pos
        self.marked = marked
        self.page = page
        self.highlight = 0
        # The first page's row a submenu was opened from, highlighted again on the way back.
        self.parent_highlight = 0


class MenuItem:
    def __init__(
        self,
        label: str,
        action=None,
        page: str | None = None,
        enabled: bool = True,
        buttons=(),
        keep_open: bool = False,
        kind: str = "item",
        icon=None,
    ):
        self.label = label
        # "item"; "heading" (a jump list category) or "separator", which do nothing.
        self.kind = kind
        # (jump list entry, its app's id): the entry's icon goes in the icon column.
        self.icon = icon
        # Runs after the frame; or `page` opens a submenu instead.
        self.action = action
        self.page = page
        self.enabled = enabled and (action is not None or page is not None)
        # Icon buttons at the row's end, as (kind, action): "pin", "unpin", "remove".
        self.buttons = list(buttons)
        # Runs without closing the menu (the buttons' actions).
        self.keep_open = keep_open


def describe(resp: "egui.Response", typ, label: str, enabled: bool = True, selected: bool | None = None):
    """Give a custom-painted control an accessibility node (role, name, state), so
    UI Automation clients such as windows-hinting can find and click it."""
    try:
        if selected is None:
            info = egui.WidgetInfo.labeled(typ, enabled, label)
        else:
            info = egui.WidgetInfo.selected(typ, enabled, selected, label)
        resp.widget_info(info)
    except Exception as e:  # never let accessibility break drawing
        print(f"thumbnail_switcher: widget_info failed: {e!r}")


def hit(ui: "egui.Ui", rect: "egui.Rect", key: str) -> "egui.Response":
    """A clickable area with a stable id (so its accessibility node is stable across
    frames) that doesn't move the layout cursor."""
    return ui.interact(rect, egui.Id(f"ts:{key}"), egui.Sense.click())


def menu_row_height(item: "MenuItem") -> float:
    return MENU_SEPARATOR_HEIGHT if item.kind == "separator" else MENU_ITEM_HEIGHT


def menu_sections(*groups: list["MenuItem"]) -> list["MenuItem"]:
    """The non-empty groups of items, with separators between them."""
    items = []
    for group in groups:
        if group:
            if items:
                items.append(MenuItem("", kind="separator"))
            items.extend(group)
    return items


def menu_number_of(item: "MenuItem") -> bool:
    """Whether a menu item gets a number: enabled ones, except going back."""
    return item.enabled and item.page != "main"


def menu_numbers(items: list["MenuItem"]) -> list[int | None]:
    """Each item's number on its page (1-based), or None."""
    numbers, n = [], 0
    for item in items:
        if menu_number_of(item):
            n += 1
            numbers.append(n)
        else:
            numbers.append(None)
    return numbers


class Placement:
    """Filling a layout's slots one window at a time."""

    def __init__(self, layout: str, slots: list[str], screen: ui.Screen):
        self.layout = layout
        self.slots = slots
        self.screen = screen
        self.index = 0
        # Window handle -> the slot it was put in.
        self.placed: dict[int, str] = {}

    @property
    def slot(self) -> str:
        return self.slots[self.index]


def slot_label(slot: str) -> str:
    return slot.lower().replace("_", " ")


def slot_fractions(slot: str):
    """(left, top, right, bottom) of a snap position, from community's window_snap.py."""
    snap = sys.modules.get("user.community.core.windows_and_tabs.window_snap")
    pos = snap._snap_positions[slot]
    return pos.left, pos.top, pos.right, pos.bottom


def slot_rect(screen: ui.Screen, slot: str) -> ui.Rect:
    left, top, right, bottom = slot_fractions(slot)
    r = screen.visible_rect
    return ui.Rect(
        round(r.x + r.width * left),
        round(r.y + r.height * top),
        round(r.width * (right - left)),
        round(r.height * (bottom - top)),
    )


class SlotOverlay:
    """A frame on screen around the slot the next window goes to.

    A separate, never-focused egui window shaped to just the frame, so the switcher
    keeps the keyboard and the inside stays visible and clickable.
    """

    def __init__(self):
        self.rect: tuple[int, int, int, int] | None = None
        self.hwnd: int | None = None
        self.showing = False
        self.window = Window()
        self.window.title = OVERLAY_TITLE
        self.window.decorated = False
        self.window.resizable = False
        self.window.draggable = False
        self.window.autosize = False
        self.window.toplevel = True
        self.window.focusable = False
        self.window.set_content(self.render)

    def show(self, rect: ui.Rect):
        self.rect = (int(rect.x), int(rect.y), int(rect.x + rect.width), int(rect.y + rect.height))
        self.showing = True
        self.window.show()
        self.place()

    def place(self):
        """Fit the native window to the slot; called again from the switcher's tick."""
        if not self.showing or self.rect is None:
            return
        if self.hwnd is None or not dwm.is_window(self.hwnd):
            self.hwnd = dwm.find_own_hwnd(OVERLAY_TITLE)
            if self.hwnd is None:
                return
        if dwm.hwnd_rect(self.hwnd) != self.rect:
            dwm.move_hwnd(self.hwnd, self.rect)
            left, top, right, bottom = self.rect
            dwm.make_overlay(self.hwnd, right - left, bottom - top, OVERLAY_THICKNESS)

    def hide(self):
        self.showing = False
        self.window.hide()

    async def render(self, ui: egui.Ui) -> None:
        ui.painter().rect_filled(ui.clip_rect(), 0, SELECTED)

    def close(self):
        self.hide()
        self.window.close()


class GridOverlay:
    """Placing windows into a layout: the screen dimmed a little, with every slot of
    the layout outlined and the current one filled in. A click-through layer under
    the switcher and the slot's frame (which are topmost), and under the windows
    already placed, so they show at full brightness landing in their slots; not
    topmost itself, so placed windows can go above it."""

    # How much the layer covers what's below, of 255: about 40%, so windows behind
    # show through at about 60% brightness. Lines and numbers are drawn bright to
    # stay readable through it.
    ALPHA = 105

    def __init__(self):
        self.rect: tuple[int, int, int, int] | None = None
        self.cells: list[tuple[int, int, int, int]] = []
        self.current = 0
        self.repaints = 0
        self.hwnd: int | None = None
        self.showing = False
        self.window = Window()
        self.window.title = GRID_OVERLAY_TITLE
        self.window.decorated = False
        self.window.resizable = False
        self.window.draggable = False
        self.window.autosize = False
        self.window.toplevel = False
        self.window.focusable = False
        self.window.set_content(self.render)

    def show(self, screen_rect: ui.Rect, cells: list[ui.Rect], current: int):
        """`screen_rect` and `cells` in physical pixels; `current` is the slot to fill."""
        self.rect = (int(screen_rect.x), int(screen_rect.y), int(screen_rect.x + screen_rect.width), int(screen_rect.y + screen_rect.height))
        self.cells = [(int(c.x), int(c.y), int(c.x + c.width), int(c.y + c.height)) for c in cells]
        self.current = current
        self.showing = True
        self.window.show()
        self.place()
        # The window shows a frame late (see Switcher.refresh): without the extra
        # frame, a new layout would appear with the previous one's cells.
        self.repaints = 2
        self.window.refresh()

    def place(self, above: int | None = None):
        """Fit the native window to the screen and keep it right below `above` (a
        placed window), or at the top of the ordinary windows."""
        if not self.showing or self.rect is None:
            return
        if self.hwnd is None or not dwm.is_window(self.hwnd):
            self.hwnd = dwm.find_own_hwnd(GRID_OVERLAY_TITLE)
            if self.hwnd is None:
                return
        if not dwm.is_layered(self.hwnd):
            # Talon/winit can reset the extended styles (on show); without them the
            # layer is opaque.
            dwm.make_scrim(self.hwnd, self.ALPHA)
        if dwm.hwnd_rect(self.hwnd) != self.rect:
            dwm.move_hwnd(self.hwnd, self.rect)
        if above is not None:
            dwm.place_below(self.hwnd, above)
        else:
            dwm.raise_quietly(self.hwnd, topmost=False)

    def hide(self):
        self.showing = False
        self.window.hide()

    async def render(self, ui: egui.Ui) -> None:
        if self.repaints > 0:
            self.repaints -= 1
            if self.repaints:
                ui.ctx().request_repaint()
        painter = ui.painter()
        painter.rect_filled(ui.clip_rect(), 0, egui.Color32.from_rgb(0, 0, 0))
        if self.rect is None or self.hwnd is None:
            return
        ppp = (dwm.user32.GetDpiForWindow(self.hwnd) or 96) / 96
        left, top = self.rect[0], self.rect[1]
        for i, (l, t, r, b) in enumerate(self.cells):
            cell = egui.Rect.from_min_max(
                egui.Pos2((l - left) / ppp + 4, (t - top) / ppp + 4), egui.Pos2((r - left) / ppp - 4, (b - top) / ppp - 4)
            )
            if i == self.current:
                painter.rect_filled(cell, 10, egui.Color32.from_rgb(60, 140, 255))
                painter.rect_stroke(cell, 10, egui.Stroke(8.0, egui.Color32.from_rgb(120, 190, 255)), egui.StrokeKind.Inside)
            else:
                painter.rect_stroke(cell, 10, egui.Stroke(5.0, egui.Color32.from_rgb(255, 255, 255)), egui.StrokeKind.Inside)
            painter.text(cell.center(), egui.Align2.CENTER_CENTER, str(i + 1), egui.FontId.proportional(80.0), egui.Color32.from_rgb(255, 255, 255))

    def close(self):
        self.hide()
        self.window.close()


def app_names(window: ui.Window) -> tuple[str, str]:
    """The window's (app name, executable file name)."""
    try:
        return window.app.name, os.path.basename(window.app.exe)
    except Exception:
        return "", ""


def resolve_app(apps: list[tuple[str, str]], text: str) -> str | None:
    """The app name among (app name, exe name) pairs that best matches `text`."""
    text = text.strip().lower()
    if not text:
        return None
    names = list(dict.fromkeys(name for name, _exe in apps if name))
    exes = {name: exe.lower() for name, exe in apps}
    for test in (
        lambda name: name.lower() == text,
        lambda name: name.lower().startswith(text),
        lambda name: exes.get(name, "").startswith(text),
        lambda name: any(word.startswith(text) for word in name.lower().split()),
        lambda name: text in name.lower() or text in exes.get(name, ""),
    ):
        found = [name for name in names if test(name)]
        if found:
            return found[0]
    return None


def app_chip(entries: list[Entry], name: str) -> Chip | None:
    """A chip for every window of the app called `name` (case-insensitive)."""
    hwnds = [e.hwnd for e in entries if e.app_name.lower() == name.lower()]
    return Chip(name, hwnds) if hwnds else None


def is_candidate(window: ui.Window) -> bool:
    try:
        return (
            bool(window.title)
            # Talon's own windows: the HUD, this switcher, ...
            and dwm.window_pid(window.id) != os.getpid()
            and is_switchable(window.id)
        )
    except Exception:
        return False


def sort_by_z_order(windows: list[ui.Window]) -> list[ui.Window]:
    order = dwm.z_order()
    return sorted(windows, key=lambda w: order.get(w.id, len(order)))


def all_windows() -> list[ui.Window]:
    """Every open or minimized top-level window, on any virtual desktop.

    ui.windows() rather than each foreground app's windows: an app whose windows are
    all on other desktops counts as a background app.
    """
    windows = [w for w in ui.windows() if is_candidate(w)]
    # A window can be listed twice, e.g. a console under cmd and conhost; keep the
    # first window object.
    unique = {w.id: w for w in reversed(windows)}
    return sort_by_z_order(list(unique.values()))


def application_windows(name: str) -> list[ui.Window]:
    """Windows for an entry of the community user.running_applications list.

    Entries are "<app name>" or "<app name>-::*::-<AppUserModelID>"; with an ID, only
    the windows carrying that ID are shown, so e.g. one PWA hosted by a browser.
    """
    splits = name.split("-::*::-")
    app_name = splits[0]
    model_id = splits[1] if len(splits) > 1 and splits[1] != "None" else None

    try:
        found = actions.user.get_running_app(app_name)
    except Exception:
        found = [a for a in ui.apps(background=False) if a.name.lower() == app_name.lower()]

    windows = []
    for item in found:
        if isinstance(item, ui.Window):
            # The app switcher maps an app's entry to exactly its windows (one MMC
            # console, one PWA), not to all windows of their process.
            candidates = [item]
        else:
            candidates = item.windows()
        windows.extend(w for w in candidates if is_candidate(w))

    if model_id:
        matching = [
            w
            for w in windows
            if str(window_model_id(w.id)).lower() == model_id.lower()
        ]
        # The default window of an app may carry no ID at all; keep everything then.
        windows = matching or windows

    unique = {w.id: w for w in windows}
    return sort_by_z_order(list(unique.values()))


def choose_grid(count: int, work: tuple[int, int, int, int], ppp: float) -> tuple[int, int, int]:
    """Pick (columns, width, height) giving the biggest tiles that fit the screen.

    Tiles don't shrink below MIN_TILE_WIDTH; past that the grid is taller than the
    window and scrolls.
    """
    work_w = (work[2] - work[0]) * SCREEN_FILL
    work_h = (work[3] - work[1]) * SCREEN_FILL
    chrome_w = 2 * PADDING * ppp
    chrome_h = (HEADER_HEIGHT + SEARCH_HEIGHT + 2 * PADDING) * ppp
    label_h = (LABEL_HEIGHT + PADDING) * ppp
    max_tile_w = (work[2] - work[0]) * MAX_TILE_WIDTH_FRACTION
    min_tile_w = min(MIN_TILE_WIDTH * ppp, work_w - chrome_w)
    max_cols = max(int((work_w - chrome_w) // min_tile_w), 1)

    best = (0.0, 1)
    for cols in range(1, min(max(count, 1), max_cols) + 1):
        rows = math.ceil(count / cols)
        tile_w = min((work_w - chrome_w) / cols, max_tile_w)
        tile_h = tile_w / TILE_ASPECT + label_h
        if rows * tile_h > work_h - chrome_h:
            tile_h = (work_h - chrome_h) / rows
            tile_w = max(min(tile_w, (tile_h - label_h) * TILE_ASPECT), min_tile_w)
        # At the minimum size, more columns means less scrolling.
        if (tile_w, cols) > best:
            best = (tile_w, cols)

    tile_w, cols = best
    rows = math.ceil(count / cols)
    tile_h = tile_w / TILE_ASPECT + label_h
    width = int(cols * tile_w + chrome_w)
    height = int(min(rows * tile_h + chrome_h, work_h))
    return cols, width, height


def choose_apps(count: int, work: tuple[int, int, int, int], ppp: float) -> tuple[int, int, int]:
    """Pick (columns, width, height) for the apps view: a strip of icons, wrapping."""
    work_w = (work[2] - work[0]) * SCREEN_FILL
    work_h = (work[3] - work[1]) * SCREEN_FILL
    chrome_w = 2 * PADDING * ppp
    chrome_h = (HEADER_HEIGHT + SEARCH_HEIGHT + 2 * PADDING) * ppp
    cell = APP_CELL * ppp
    cols = max(1, min(count, APP_MAX_COLUMNS, int((work_w - chrome_w) // cell)))
    width = max(cols * cell + chrome_w, APPS_MIN_WIDTH * ppp)
    # Cells stretch to the width; rows are as tall as cells are wide.
    cell_w = (width - chrome_w) / cols
    rows = math.ceil(count / cols)
    height = min(max(rows * cell_w + chrome_h, APPS_MIN_HEIGHT * ppp), work_h)
    return cols, int(width), int(height)


def text_points(text: str, font_size: float) -> float:
    """Rough width of `text`; the same estimate elide() uses."""
    return len(text) * 0.55 * font_size


def choose_list(entries: list["Entry"], work: tuple[int, int, int, int], ppp: float) -> tuple[int, int]:
    """Pick (width, height) for the list view: as wide as the longest row, up to a cap."""
    longest = max(
        (text_points(e.title, 14.0) + text_points(e.app_label(), 13.0) for e in entries),
        default=0.0,
    )
    row_w = 10 + NUMBER_WIDTH + ROW_ICON + 10 + longest + 24 + 10
    width = max(row_w + 3 * PADDING, LIST_MIN_WIDTH) * ppp
    width = min(width, (work[2] - work[0]) * LIST_MAX_WIDTH_FRACTION)
    height = (
        HEADER_HEIGHT + SEARCH_HEIGHT + 2 * PADDING + len(entries) * (ROW_HEIGHT + ROW_GAP)
    ) * ppp
    height = min(height, (work[3] - work[1]) * SCREEN_FILL)
    return int(width), int(height)


def fit(src_w: int, src_h: int, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Largest rectangle with the source's aspect ratio centered inside `box`."""
    left, top, right, bottom = box
    box_w, box_h = right - left, bottom - top
    if src_w <= 0 or src_h <= 0 or box_w <= 0 or box_h <= 0:
        return box
    scale = min(box_w / src_w, box_h / src_h)
    w, h = int(src_w * scale), int(src_h * scale)
    x = left + (box_w - w) // 2
    y = top + (box_h - h) // 2
    return (x, y, x + w, y + h)


def to_pixels(rect: egui.Rect, ppp: float) -> tuple[int, int, int, int]:
    """An egui rect in points as (left, top, right, bottom) physical pixels."""
    return (
        int(rect.min.x * ppp),
        int(rect.min.y * ppp),
        int(rect.max.x * ppp),
        int(rect.max.y * ppp),
    )


def elide(text: str, width_points: float, font_size: float) -> str:
    max_chars = max(int(width_points / (0.55 * font_size)), 4)
    return text if len(text) <= max_chars else text[: max_chars - 1] + "…"


class Switcher:
    def __init__(self):
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
        # Frames still to draw after a change; see refresh().
        self.repaints = 0
        # UI Automation (AccessKit) is turned on with the first frame.
        self.accesskit = False

        self.window = Window()
        self.window.title = WINDOW_TITLE
        self.window.decorated = False
        self.window.resizable = False
        self.window.draggable = False
        self.window.autosize = False
        self.window.toplevel = True
        # Takes keyboard focus while showing, for the arrow keys, Enter and Escape.
        self.window.focusable = True
        self.window.set_content(self.render)
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
            self.previous_foreground = dwm.foreground()
        work = dwm.foreground_work_area()
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
        self.window.show()
        if self.hwnd is not None and not dwm.is_window(self.hwnd):
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
        self.window.hide()
        self._update_tags()

    def refresh(self):
        """Redraw after a change. The window shows a frame late: what a refresh draws
        only appears with the next frame, so this asks for one more."""
        self.repaints = 2
        self.window.refresh()

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
        if list(ctx.tags) != tags:
            ctx.tags = tags

    def cancel(self):
        """Close the switcher and give focus back to the window the user came from."""
        # Focus first: hiding the switcher while it is foreground would let Windows
        # activate whatever window is next in z-order.
        if self.previous_foreground is not None and dwm.is_window(self.previous_foreground):
            dwm.set_foreground(self.previous_foreground)
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
        dwm.set_foreground(last.hwnd)
        self.hide()

        def check():
            if dwm.foreground() != last.hwnd:
                try:
                    actions.user.switcher_focus_window(last.window)
                except Exception:
                    dwm.set_foreground(last.hwnd)

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
        dwm.set_foreground(entries[0].hwnd)
        self.hide()
        # Raise the others quickly; only the last one needs to end up with focus.
        for entry in entries[1:]:
            dwm.set_foreground(entry.hwnd)
        last = entries[-1]
        try:
            actions.user.switcher_focus_window(last.window)
        except Exception as e:
            print(f"thumbnail_switcher: focusing {last.title!r} failed: {e!r}")
            last.window.focus()

    # --- managing windows by number ---
    # All of these leave the switcher open, focused and on the same tile.

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

    # --- marking several windows ---
    # Marks pick the windows the marked-window commands, the header's buttons, the
    # marked windows' menu and Delete act on; focusing still takes one window.

    def _set_marks(self, entries: list, on: bool | None):
        """Mark (True), unmark (False) or toggle (None) these tiles; with the lock held."""
        for entry in entries:
            hwnds = tile_hwnds(entry)
            add = on if on is not None else not all(h in self.marked for h in hwnds)
            if add:
                self.marked += [h for h in hwnds if h not in self.marked]
            else:
                self.marked = [h for h in self.marked if h not in hwnds]
            self.mark_anchor = entry.hwnd

    def mark(self, indices: list[int], on: bool | None = None):
        """Toggle the marks of the tiles with these numbers; or set them with `on`."""
        with self.lock:
            self._set_marks([self.entries[i - 1] for i in indices if 0 < i <= len(self.entries)], on)
        self.refresh()

    def mark_range(self, first: int, last: int):
        """Mark tiles `first` through `last` (numbers, either order)."""
        self.mark(list(range(min(first, last), max(first, last) + 1)), on=True)

    def mark_to(self, index: int):
        """Shift+click: mark from the last marked (or the selected) tile to tile `index`."""
        with self.lock:
            anchor = next((i + 1 for i, e in enumerate(self.entries) if e.hwnd == self.mark_anchor), self.selected + 1)
        self.mark_range(anchor, index)

    def mark_all(self):
        """Mark every tile the search shows."""
        with self.lock:
            self._set_marks(self.entries, True)
        self.refresh()

    def clear_marks(self):
        with self.lock:
            self.marked = []
            self.mark_anchor = None
        self.refresh()

    def marked_entries(self) -> list[Entry]:
        """The marked windows in the order they were marked, shown or not."""
        with self.lock:
            by_hwnd = {e.hwnd: e for e in self.pool}
            return [by_hwnd[h] for h in self.marked if h in by_hwnd]

    def _targets(self, fallback: bool) -> tuple[list[Entry], bool]:
        """The marked windows, and whether they are marked ones; with none marked and
        `fallback`, the selected tile's window(s)."""
        marked = self.marked_entries()
        if marked or not fallback:
            return marked, bool(marked)
        with self.lock:
            entry = self.entries[self.selected] if 0 <= self.selected < len(self.entries) else None
        return (list(getattr(entry, "windows", [entry])) if entry is not None else []), False

    def close_marked(self, fallback: bool = False):
        """Close the marked windows (or with `fallback` and none marked, the selected one).
        The marks go with the windows as they close; one that stays open (asking to save)
        stays marked."""
        entries, marked = self._targets(fallback)
        if entries:
            self.close_windows(entries=entries)

    def minimize_marked(self):
        entries, marked = self._targets(False)
        if entries:
            self.minimize_windows(entries=entries)

    def restore_marked(self):
        entries, marked = self._targets(False)
        if entries:
            self.restore_windows(entries=entries)

    def layout_marked(self, layout: str):
        """Snap the marked windows into `layout`'s positions, in the order they were
        marked; they stay marked (only closing and clearing unmark)."""
        entries, marked = self._targets(False)
        if entries:
            self.layout_windows([], LAYOUTS[layout], entries=entries)

    def move_marked_to_desktop(self, number: int | None = None, offset: int = 0):
        """Move the marked windows to a desktop; they stay marked."""
        entries, marked = self._targets(False)
        if entries:
            self.move_to_desktop([], number=number, offset=offset, entries=entries)

    def move_marked_to_new_desktop(self):
        try:
            desktop = vd.create_desktop()
        except OSError as e:
            app.notify("Thumbnail switcher", f"Couldn't create a desktop: {e}")
            return
        with self.lock:
            self.desktops, self.current_desktop = self._read_desktops()
        self.move_marked_to_desktop(number=desktop.number)

    def move_marked_to_screen(self, screen: int | None = None, offset: int = 0):
        """Move the marked windows to a screen; they stay marked."""
        entries, marked = self._targets(False)
        if not entries:
            return
        self._hold_focus()
        for entry in entries:
            self._move_window_to_screen(entry, screen, offset)
        self._take_focus()
        self.sync()

    def open_marked_menu(self, pos: "egui.Pos2 | None" = None, page: str = "main"):
        """Open the marked windows' menu (or one of its submenus), if any are marked."""
        if not self.marked_entries():
            return
        with self.lock:
            self.menu = Menu(None, pos, marked=True, page=page)
        self.refresh()
        self._update_tags()

    def open_bar_dropdown(self, page: str):
        """Open a marked bar button's dropdown ("snap", "layout", "desktop", "screen")
        under the button, on its first item: by click and by voice alike."""
        entries = self.marked_entries()
        if not entries:
            return
        if (page == "snap") != (len(entries) == 1) and page in ("snap", "layout"):
            # Snap is for one marked window, a layout for several: the bar shows one.
            app.notify("Thumbnail switcher", "Snap one marked window; say layout for several" if page == "snap" else "Layout needs two or more marked windows; say snap")
            return
        menu = Menu(None, self.bar_anchors.get(page), marked=True, page=page, dropdown=True)
        items = self._marked_menu_items(page, dropdown=True)
        menu.highlight = next((i for i, it in enumerate(items) if it.enabled), 0)
        with self.lock:
            self.menu = menu
        self.refresh()
        self._update_tags()

    def _marked_menu_items(self, page: str, dropdown: bool | None = None) -> list[MenuItem]:
        """The marked windows' menu; a bar dropdown's pages have no "< Back"."""
        if dropdown is None:
            dropdown = bool(self.menu is not None and self.menu.dropdown)
        items = self._marked_menu_page(page)
        return [item for item in items if item.page != "main"] if dropdown else items

    def _marked_menu_page(self, page: str) -> list[MenuItem]:
        entries = self.marked_entries()
        back = MenuItem("<  Back", page="main")
        if page == "snap":
            return [back] + [
                MenuItem(slot_label(slot).capitalize(), lambda slot=slot: self.layout_windows([], [slot], entries=entries[:1]))
                for slot in MENU_SNAPS
            ]
        if page == "layout":
            return [back] + [
                MenuItem(f"{layout.replace('_', ' ').capitalize()} ({len(slots)})", lambda layout=layout: self.layout_marked(layout))
                for layout, slots in LAYOUTS.items()
            ]
        if page == "desktop":
            items = [back]
            for desktop in self.desktops:
                items.append(
                    MenuItem(
                        desktop.label(),
                        lambda n=desktop.number: self.move_marked_to_desktop(number=n),
                        enabled=any(e.desktop_number != desktop.number for e in entries),
                    )
                )
            items.append(MenuItem("New desktop", self.move_marked_to_new_desktop))
            return items
        if page == "screen":
            items = [back]
            for n in range(1, self.screen_count + 1):
                items.append(
                    MenuItem(
                        f"Screen {n}",
                        lambda n=n: self.move_marked_to_screen(screen=n),
                        enabled=any(e.screen_number != n for e in entries),
                    )
                )
            items.append(MenuItem("Next screen", lambda: self.move_marked_to_screen(offset=1)))
            items.append(MenuItem("Previous screen", lambda: self.move_marked_to_screen(offset=-1)))
            return items
        count = len(entries)
        return [
            # A heading, not an item: disabled, so it has no number.
            MenuItem(f"{count} marked window{'s' if count != 1 else ''}"),
            MenuItem("Close all", self.close_marked),
            MenuItem("Minimize all", self.minimize_marked, enabled=any(not e.minimized for e in entries)),
            MenuItem("Restore all", self.restore_marked, enabled=any(e.minimized for e in entries)),
            # One window snaps; several make a layout.
            MenuItem("Snap  >", page="snap") if count == 1 else MenuItem("Layout  >", page="layout"),
            MenuItem("Move to desktop  >", page="desktop", enabled=vd.available()),
            *([MenuItem("Move to screen  >", page="screen")] if self.screen_count > 1 else []),
            MenuItem("Clear marks", self.clear_marks),
        ]

    # --- the right-click menu ---

    def open_menu(self, index: int, pos: "egui.Pos2 | None" = None):
        """Open the menu for tile `index` (1-based), at `pos` or at the tile."""
        with self.lock:
            if not 0 < index <= len(self.entries):
                return
            self.selected = index - 1
            self.menu = Menu(self.entries[index - 1].hwnd, pos)
        self.refresh()
        self._update_tags()

    def close_menu(self):
        with self.lock:
            self.menu = None
        self.refresh()
        self._update_tags()

    def menu_back(self):
        """Back from a submenu to the menu's first page (a bar dropdown has none)."""
        with self.lock:
            if self.menu is not None and not self.menu.dropdown:
                self.menu.page, self.menu.highlight = "main", self.menu.parent_highlight
        self.refresh()

    def _menu_entry(self, menu: Menu | None) -> "Entry | AppGroup | None":
        """The tile the menu is for; None for the marked windows' menu. Lock held."""
        if menu is None or menu.marked:
            return None
        return next((e for e in self.entries if e.hwnd == menu.hwnd), None)

    def menu_key(self, key: str):
        """Up/Down (Home/End) move the highlight over enabled items, Enter picks, Right
        opens the highlighted submenu, Left goes back from one."""
        with self.lock:
            menu = self.menu
            entry = self._menu_entry(menu)
        if menu is None or (entry is None and not menu.marked):
            return
        items = self._menu_items(entry, menu.page)
        enabled = [i for i, item in enumerate(items) if item.enabled]
        if not enabled:
            return
        highlighted = items[menu.highlight] if menu.highlight < len(items) else None
        if key == "Enter":
            if highlighted is not None:
                self._pick(menu, highlighted)
            return
        if menu.dropdown and key in ("ArrowLeft", "ArrowRight"):
            # Like a menu bar: the neighbouring button's dropdown.
            pages = list(self.bar_anchors)
            if menu.page in pages and len(pages) > 1:
                step = 1 if key == "ArrowRight" else -1
                self.open_bar_dropdown(pages[(pages.index(menu.page) + step) % len(pages)])
            return
        if key == "ArrowRight":
            if highlighted is not None and highlighted.enabled and highlighted.page not in (None, "main"):
                self._pick(menu, highlighted)
            return
        if key == "ArrowLeft":
            if menu.page != "main":
                self.menu_back()
            return
        if key in ("Home", "End"):
            menu.highlight = enabled[0] if key == "Home" else enabled[-1]
            self.refresh()
            return
        step = 1 if key == "ArrowDown" else -1
        later = [i for i in enabled if (i - menu.highlight) * step > 0]
        menu.highlight = (min(later) if step > 0 else max(later)) if later else (enabled[0] if step > 0 else enabled[-1])
        self.refresh()

    def pick_menu_item(self, number: int):
        """Pick the open menu's item `number`, as numbered on its current page."""
        with self.lock:
            menu = self.menu
            entry = self._menu_entry(menu)
        if menu is None or (entry is None and not menu.marked):
            return
        numbered = [item for item in self._menu_items(entry, menu.page) if menu_number_of(item)]
        if 0 < number <= len(numbered):
            self._pick(menu, numbered[number - 1])

    def _pick(self, menu: Menu, item: MenuItem):
        if not item.enabled:
            return
        if item.page is not None:
            if item.page == "main":
                self.menu_back()
                return
            if menu.page == "main":
                menu.parent_highlight = menu.highlight
            menu.page = item.page
            # On its first item, past "< Back".
            with self.lock:
                entry = self._menu_entry(menu)
            items = self._menu_items(entry, menu.page) if entry is not None or menu.marked else []
            menu.highlight = next((i for i, it in enumerate(items) if it.enabled and it.page != "main"), 0)
            self.refresh()
            return
        if item.keep_open:
            # A row's button (pin, unpin, remove): the page updates in place.
            item.action()
            self.refresh()
            return
        self.close_menu()
        item.action()

    def menu_button(self, kind: str, number: int):
        """Voice for a menu row's button: "pin 3", "unpin 1", "remove 2"."""
        with self.lock:
            menu = self.menu
            entry = self._menu_entry(menu)
        if menu is None or (entry is None and not menu.marked):
            return
        numbered = [item for item in self._menu_items(entry, menu.page) if menu_number_of(item)]
        if 0 < number <= len(numbered):
            action = next((a for k, a in numbered[number - 1].buttons if k == kind), None)
            if action is not None:
                action()
                self.refresh()

    def _menu_items(self, entry: "Entry | None", page: str) -> list[MenuItem]:
        """The menu's items; actions find the window's tile number when they run. With
        no entry, the marked windows' menu."""
        if entry is None:
            return self._marked_menu_items(page)

        def number() -> int:
            with self.lock:
                return next((i + 1 for i, e in enumerate(self.entries) if e.hwnd == entry.hwnd), 0)

        if page.startswith("jump"):
            return self._jump_menu(entry, page)
        # Left out when the app has no jump list.
        jump_items = [MenuItem("Jump list  >", page="jump:0")] if self._has_jump_list(entry) else []
        # Its launch_applications.json entry; none for apps not in the launch list
        # (Console1, portable apps), so the item is left out for those.
        entry_id = self._launch_entry_id(entry)
        edit_items = [MenuItem("Edit launch entry...", lambda: self._edit_launch_entry(entry_id))] if entry_id else []
        if isinstance(entry, launcher_apps.InstalledApp):
            return menu_sections([MenuItem("Launch", lambda: self.launch(number()) if number() else None)], jump_items + edit_items)
        if isinstance(entry, AppGroup):
            if page == "desktop":
                items = [MenuItem("<  Back", page="main")]
                for desktop in self.desktops:
                    items.append(
                        MenuItem(
                            desktop.label(),
                            lambda n=desktop.number: self.move_app_to_desktop(entry, n),
                            enabled=any(w.desktop_number != desktop.number for w in entry.windows),
                        )
                    )
                return items
            if page == "screen":
                return self._screen_menu(number, here=None)
            if page == "snap":
                # Its most recent window, like the window menu's Snap.
                return [MenuItem("<  Back", page="main")] + [
                    MenuItem(slot_label(slot).capitalize(), lambda slot=slot: self.snap_window(number(), slot))
                    for slot in MENU_SNAPS
                ]
            if page == "layout":
                # All its windows, most recent first, like the marked windows' layouts.
                return [MenuItem("<  Back", page="main")] + [
                    MenuItem(
                        f"{layout.replace('_', ' ').capitalize()} ({len(slots)})",
                        lambda layout=layout: self.layout_windows([], LAYOUTS[layout], entries=entry.windows),
                    )
                    for layout, slots in LAYOUTS.items()
                ]
            # The window menu's items for all of the app's windows (one source for the
            # apps strip and the launcher), plus app ones.
            any_minimized = any(w.minimized for w in entry.windows)
            all_minimized = all(w.minimized for w in entry.windows)
            return menu_sections(
                [
                    MenuItem("Focus", lambda: self.select(number()) if number() else None),
                    MenuItem("Launch new window", lambda: self.launch(number()) if number() else None),
                    MenuItem("Show windows", lambda: self.show_app_windows(number()) if number() else None),
                ],
                [
                    MenuItem(
                        "Close all windows" if len(entry.windows) > 1 else "Close",
                        lambda: self.close_windows([number()]),
                    ),
                    MenuItem("Restore all" if len(entry.windows) > 1 else "Restore", lambda: self.restore_windows(entries=entry.windows), enabled=any_minimized),
                    MenuItem("Minimize all" if len(entry.windows) > 1 else "Minimize", lambda: self.minimize_windows(entries=entry.windows), enabled=not all_minimized),
                    MenuItem("Maximize", lambda: self.maximize_window(number())),
                ],
                [
                    # One window snaps; several make a layout.
                    *([MenuItem("Snap  >", page="snap")] if len(entry.windows) == 1 else []),
                    *([MenuItem("Layout  >", page="layout")] if len(entry.windows) > 1 else []),
                    MenuItem("Move all to desktop  >", page="desktop", enabled=vd.available() and len(self.desktops) > 1),
                    *([MenuItem("Move all to screen  >", page="screen")] if self.screen_count > 1 else []),
                ],
                jump_items + edit_items,
            )
        if page == "screen":
            return self._screen_menu(number, here=entry.screen_number)
        if page == "snap":
            return [MenuItem("<  Back", page="main")] + [
                MenuItem(slot_label(slot).capitalize(), lambda slot=slot: self.snap_window(number(), slot))
                for slot in MENU_SNAPS
            ]
        if page == "desktop":
            items = [MenuItem("<  Back", page="main")]
            for desktop in self.desktops:
                current = desktop.guid.key() == entry.desktop_key
                items.append(
                    MenuItem(
                        desktop.label() + (" (here)" if current else ""),
                        lambda n=desktop.number: self.move_to_desktop([number()], number=n),
                        enabled=not current,
                    )
                )
            items.append(MenuItem("New desktop", lambda: self.move_to_new_desktop(number())))
            return items
        return menu_sections(
            [
                MenuItem("Focus", lambda: self._activate(self.entries_at([number()])) if number() else None),
                MenuItem("Close", lambda: self.close_windows([number()])),
                MenuItem("Restore", lambda: self.restore_windows([number()]))
                if entry.minimized
                else MenuItem("Minimize", lambda: self.minimize_windows([number()])),
                MenuItem("Maximize", lambda: self.maximize_window(number())),
            ],
            [
                MenuItem("Snap  >", page="snap"),
                MenuItem("Move to desktop  >", page="desktop", enabled=vd.available()),
                *([MenuItem("Move to screen  >", page="screen")] if self.screen_count > 1 else []),
            ],
            [MenuItem(f"Filter to {entry.app_name}", lambda: self.set_app(entry.app_name), enabled=bool(entry.app_name))] + jump_items,
        )

    def _jump_ids(self, entry) -> list[str]:
        """The ids a tile's jump list may be filed under, best first: the window's or
        process's AppUserModelID (Steam sets "Valve.Steam.Client"), the MMC console's,
        the launch list's, the Start menu entry of its executable (VS Code)."""
        if isinstance(entry, launcher_apps.InstalledApp):
            return [entry.app_id]
        identity = app_identity.resolve(entry.hwnd, getattr(entry, "talon_app_name", entry.app_name))
        ids = [identity.window_id, identity.process_id, identity.document_id]
        launch = getattr(entry, "launch", None)
        if launch is not None:
            ids.append(launch.app_id)
        if identity.exe_path:
            ids.append(shell_apps.app_id_for_path(identity.exe_path))
        return [i for i in ids if i]

    def _launch_entry_id(self, entry) -> str | None:
        """The app's unique_identifier in launch_applications.json, if it has an entry."""
        community = sys.modules.get(launcher_apps.COMMUNITY)
        overrides = getattr(community, "APPLICATIONS_OVERRIDES", None) if community else None
        if not overrides:
            return None
        candidates = [launch_id(entry)]
        if not isinstance(entry, launcher_apps.InstalledApp):
            candidates += self._jump_ids(entry)
        for candidate in candidates:
            found = overrides.get(candidate.lower()) if candidate else None
            if found is not None and getattr(found, "unique_identifier", None):
                return found.unique_identifier
        return None

    def _edit_launch_entry(self, app_id: str):
        """Close the switcher and open the launch applications editor on the entry."""
        self.hide()
        try:
            actions.user.launch_applications_editor_show_entry(app_id)
        except Exception as e:
            app.notify("Launch applications editor", f"Couldn't open it: {e}")

    def _has_jump_list(self, entry) -> bool:
        try:
            return any(jump_lists.has_jump_list(i) for i in self._jump_ids(entry))
        except Exception:
            return False

    def _jump_menu(self, entry, page: str) -> list[MenuItem]:
        """A page of the tile's jump list: category headings, numbered entries,
        separators as dividers; "jump:<n>" pages entries, "jumpremove:<n>" lists recent
        items to remove."""
        kind, _, number = page.partition(":")
        index = int(number or 0)
        jump = jump_lists.jump_list(self._jump_ids(entry))
        items = [MenuItem("<  Back", page="main")]
        if jump is None:
            return items + [MenuItem("No jump list")]
        exe = None if isinstance(entry, launcher_apps.InstalledApp) else app_identity.resolve(entry.hwnd).exe_path
        app_id = jump.app_id
        rows = []
        for category in jump.categories:
            rows.append(MenuItem(category.name, kind="heading"))
            for item in category.entries:
                if item.kind == "separator":
                    rows.append(MenuItem("", kind="separator"))
                    continue
                # Like the taskbar: pinned items can be unpinned; recent ones pinned or
                # removed; app categories' items pinned; tasks neither.
                buttons = []
                if category.kind == "pinned":
                    buttons = [("unpin", lambda item=item: jump_lists.unpin(app_id, item))]
                elif category.kind == "recent":
                    buttons = [
                        ("pin", lambda item=item: jump_lists.pin(app_id, item)),
                        ("remove", lambda item=item: jump_lists.remove(app_id, item)),
                    ]
                elif category.kind == "custom":
                    buttons = [("pin", lambda item=item: jump_lists.pin(app_id, item))]
                rows.append(MenuItem(item.title, lambda item=item: self._run_jump(item, exe), buttons=buttons, icon=(item, app_id)))
        pages = max(1, -(-len(rows) // JUMP_PAGE_ROWS))
        index = max(0, min(index, pages - 1))
        items += rows[index * JUMP_PAGE_ROWS : (index + 1) * JUMP_PAGE_ROWS]
        if index > 0:
            items.append(MenuItem("<  Previous", page=f"{kind}:{index - 1}"))
        if index < pages - 1:
            items.append(MenuItem("More  >", page=f"{kind}:{index + 1}"))
        return items

    def _run_jump(self, item, exe: str | None):
        """Open a jump list entry and close the switcher; the app takes the focus."""
        try:
            jump_lists.run(item, exe)
        except OSError as e:
            app.notify("Jump list", f"Couldn't open {item.title}: {e}")
            return
        self.hide()

    def _screen_menu(self, number, here: int | None) -> list[MenuItem]:
        """The screens submenu: each screen (the window's own greyed out), next, previous."""
        items = [MenuItem("<  Back", page="main")]
        for n in range(1, self.screen_count + 1):
            items.append(
                MenuItem(
                    f"Screen {n}" + (" (here)" if n == here else ""),
                    lambda n=n: self.move_to_screen(number(), screen=n),
                    enabled=n != here,
                )
            )
        items.append(MenuItem("Next screen", lambda: self.move_to_screen(number(), offset=1)))
        items.append(MenuItem("Previous screen", lambda: self.move_to_screen(number(), offset=-1)))
        return items

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

    # --- placing windows into a layout, slot by slot ---

    def start_placement(self, layout: str):
        """Fill `layout`'s slots on the switcher's screen; numbers now pick windows."""
        if not self.showing:
            return
        placement = Placement(layout, LAYOUTS[layout], self._screen())
        with self.lock:
            self.placement = placement
        self._show_slot()
        self.refresh()
        # Marked windows fill the first slots, in the order they were marked.
        marked = self.marked_entries()
        if marked:
            for entry in marked[: len(placement.slots)]:
                self._place(entry)

    def place(self, index: int):
        """Put the window on tile `index` into the current slot and move on."""
        entries = self.entries_at([index])
        if entries:
            self._place(entries[0])

    def _place(self, entry: Entry):
        with self.lock:
            placement = self.placement
        if placement is None:
            return
        self._hold_focus()
        try:
            if entry.away and self.current_desktop is not None:
                vd.move_window(entry.hwnd, next(d.guid for d in self.desktops if d.guid.key() == self.current_desktop))
            dwm.make_normal(entry.hwnd)
            entry.window.rect = slot_rect(placement.screen, placement.slot)
            # In front of the other windows (under the switcher and its overlays, which
            # stay on top), so it can be seen landing in its slot.
            dwm.raise_quietly(entry.hwnd)
        except Exception as e:
            print(f"thumbnail_switcher: placing {entry.title!r} failed: {e!r}")
        with self.lock:
            placement.placed[entry.hwnd] = placement.slot
        self.skip_slot()
        self._take_focus()
        self.sync()

    def skip_slot(self):
        """Move on to the next slot; after the last one, placement is done."""
        with self.lock:
            placement = self.placement
            if placement is None:
                return
            placement.index += 1
            done = placement.index >= len(placement.slots)
        if done:
            with self.lock:
                placed = [e for h in placement.placed for e in self.pool if e.hwnd == h]
            self.end_placement()
            if placed:
                # The layout is complete: show it, the last window placed focused.
                self._finish_layout(placed)
        else:
            self._show_slot()
        self.refresh()

    def end_placement(self):
        with self.lock:
            self.placement = None
        self.overlay.hide()
        self.grid_overlay.hide()
        self.refresh()

    def _show_slot(self):
        with self.lock:
            placement = self.placement
        if placement is not None:
            # Showing the grid layer (an ordinary, not topmost window) can take the
            # focus for a moment; the switcher takes it back rather than closing.
            self._hold_focus()
            try:
                self.grid_overlay.show(
                    placement.screen.visible_rect, [slot_rect(placement.screen, slot) for slot in placement.slots], placement.index
                )
                self.overlay.show(slot_rect(placement.screen, placement.slot))
                self._stack_overlays()
            except Exception as e:
                print(f"thumbnail_switcher: showing the slot outline failed: {e!r}")

    def _stack_overlays(self):
        """The switcher on top, then the slot's frame (both topmost), then the windows
        placed so far, then the dimmed grid over everything else."""
        if self.hwnd is None:
            return
        self.overlay.place()
        if self.overlay.hwnd is not None:
            dwm.place_below(self.overlay.hwnd, self.hwnd)
        with self.lock:
            placement = self.placement
            placed = [h for h in placement.placed if dwm.is_window(h)] if placement else []
        if placed and self.grid_overlay.hwnd is not None:
            # Keep every placed window above the grid, whatever reordered them since
            # (another app's window, or the app itself, coming forward), and the grid
            # right below the lowest of them.
            z = dwm.z_order()
            lowest_z = max(z.get(h, 0) for h in placed)
            ours = {self.hwnd, self.overlay.hwnd, self.grid_overlay.hwnd}
            # An ordinary window in between: raise the placed ones again, in order.
            if any(
                pos < lowest_z
                and h not in ours
                and h not in placed
                and dwm.user32.IsWindowVisible(h)
                and not dwm.is_topmost(h)
                and not dwm.is_cloaked(h)
                and not dwm.is_minimized(h)
                for h, pos in z.items()
            ):
                for h in placed:
                    dwm.raise_quietly(h)
                z = dwm.z_order()
            lowest = max(placed, key=lambda h: z.get(h, -1))
            self.grid_overlay.place(above=lowest)
        else:
            self.grid_overlay.place(above=None)

    def _screen(self) -> ui.Screen:
        """The screen the switcher is on."""
        if self.target is not None:
            x = (self.target[0] + self.target[2]) / 2
            y = (self.target[1] + self.target[3]) / 2
            for screen in ui.screens():
                r = screen.rect
                if r.x <= x < r.x + r.width and r.y <= y < r.y + r.height:
                    return screen
        return ui.main_screen()

    # --- virtual desktops ---

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
        if self.showing and self.hwnd is not None and dwm.foreground() != self.hwnd:
            dwm.set_foreground(self.hwnd)

    # --- following window changes ---

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
        gone = {e.hwnd for e in pool if not dwm.is_window(e.hwnd) or not is_switchable(e.hwnd)}
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
                self.marked = [h for h in self.marked if h not in gone or dwm.is_window(h)]
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

    # --- native window and DWM thumbnails ---

    def _tick(self):
        if not self.showing:
            return
        if self.hwnd is None:
            hwnd = dwm.find_own_hwnd(WINDOW_TITLE)
            if hwnd is None:
                return
            self.hwnd = hwnd
            self._attach()
            return
        self.ticks += 1
        # Close when the user moves on to another window, like Alt+Tab; but not when
        # one of the switcher's own commands briefly activated a window.
        has_focus = dwm.foreground() == self.hwnd
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
            if dwm.hwnd_rect(self.hwnd) != self.target:
                dwm.move_hwnd(self.hwnd, self.target)

    def _grow_for_menu(self, extra_h: float, extra_w: float):
        """Make the window `extra_h` x `extra_w` points bigger, within its monitor's work
        area (moving it up or left if needed); `menu_restore` keeps the old rect."""
        if self.hwnd is None or self.target is None or self.menu is None:
            return
        ppp = (dwm.user32.GetDpiForWindow(self.hwnd) or 96) / 96
        left, top, right, bottom = self.target
        work = dwm.work_area(self.hwnd)
        width = min(right - left + int(extra_w * ppp), work[2] - work[0])
        height = min(bottom - top + int(extra_h * ppp), work[3] - work[1])
        left = max(work[0], min(left, work[2] - width))
        top = max(work[1], min(top, work[3] - height))
        new = (left, top, left + width, top + height)
        if new == self.target:
            return
        if self.menu_restore is None:
            self.menu_restore = self.target
        self.target = new
        dwm.move_hwnd(self.hwnd, new)
        self.refresh()

    def _restore_after_menu(self):
        """Back to the size from before a menu made the window grow."""
        if self.menu is not None or self.menu_restore is None:
            return
        self.target, self.menu_restore = self.menu_restore, None
        if self.hwnd is not None and self.showing:
            dwm.move_hwnd(self.hwnd, self.target)
        self.refresh()

    def _attach(self):
        """Position the native window and register a thumbnail for every entry."""
        dwm.move_hwnd(self.hwnd, self.target)
        self.window.focus()
        if dwm.foreground() != self.hwnd:
            dwm.set_foreground(self.hwnd)
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

    # --- drawing ---

    async def render(self, ui: egui.Ui) -> None:
        if not self.accesskit:
            try:
                ui.ctx().enable_accesskit()
            except Exception as e:
                print(f"thumbnail_switcher: enable_accesskit failed: {e!r}")
            self.accesskit = True
        if self.repaints > 0:
            self.repaints -= 1
            if self.repaints:
                ui.ctx().request_repaint()
        painter = ui.painter()
        painter.rect_filled(ui.clip_rect(), 0, BACKGROUND)
        ppp = ui.ctx().pixels_per_point()

        with self.lock:
            entries = list(self.entries)
            pool_hwnds = {entry.hwnd for entry in self.pool}
            # The launcher's installed apps keep their icon textures too.
            icon_hwnds = pool_hwnds | ({a.hwnd for a in self.launch_list.apps} if self.launch_list else set())
            running_count = self.running_count if self.mode == "launcher" else None
            window_rows = self.mode == "windows" and self.window_details
            apps_rows = self.mode == "apps" and bool(self.apps_details)
            details = (self.mode == "launcher" and bool(self.launcher_details)) or window_rows or apps_rows
            if window_rows:
                sort_column, sort_reverse = self.window_sort, self.window_sort_reverse
            elif apps_rows:
                sort_column, sort_reverse = self.apps_sort, self.apps_sort_reverse
            else:
                sort_column, sort_reverse = self.launcher_sort, self.launcher_sort_reverse
            chip = self.chip
            query = self.query
            previews = self.previews
            cols = max(self.cols, 1)
            thumbnails = dict(self.thumbnails)
            current = self.selected
            target = self.target
            placement = self.placement
            placed = dict(placement.placed) if placement else {}
            desktops = list(self.desktops)
            current_desktop = self.current_desktop
            show_screens = self.screen_count > 1
            menu = self.menu
            if menu is None and self.menu_restore is not None:
                cron.after("0ms", self._restore_after_menu)
            mode = self.mode
            marked = set(self.marked) & pool_hwnds
            if bool(self.marked) != ("user.thumbnail_switcher_marked" in ctx.tags):
                # Marks come and go in many places; the marked bar's voice commands
                # follow from here.
                cron.after("0ms", self._update_tags)
            menu_entry = self._menu_entry(menu)
            if menu is not None and menu_entry is None and not (menu.marked and marked):
                # Its window (or the last marked one) went away.
                self.menu = menu = None
            if menu is not None and menu.marked and menu.page in ("snap", "layout") and (menu.page == "snap") != (len(marked) == 1):
                # Marks changed under it: Snap is for one marked window, Layout for several.
                self.menu = menu = None
            # The first frames can come before the window has its final size; scrolling
            # the selection into view then would leave the list scrolled for no reason.
            settled = target is not None and abs(
                ui.clip_rect().height() * ppp - (target[3] - target[1])
            ) < 3
            reveal = self.reveal_selected and settled
            if reveal:
                self.reveal_selected = False
            # Drop textures of windows no longer shown, here on egui's thread.
            # Jump list icons stay while a menu is open.
            stale = [key for key in self.textures if key[0] not in icon_hwnds and not (key[0] == "jump" and menu is not None)]
            dropped = [self.textures.pop(key) for key in stale]
        del dropped

        async with ui.input() as inp:
            action = self._handle_input(inp, cols, previews or mode in APP_MODES)
            # Window-relative positions only mean something once the window is in place.
            pointer_pos = inp.pointer.latest_pos()
            pointer_moving = settled and self._pointer_moved(pointer_pos)
            primary_clicked = inp.pointer.primary_clicked()
            # Only a mouse that is moving now takes the menu highlight from the keyboard.
            pointer_moving_now = inp.pointer.is_moving()
            wheel = inp.raw_scroll_delta.y
            # For Ctrl+click and Shift+click.
            ctrl_down = bool(inp.modifiers.ctrl)
            shift_down = bool(inp.modifiers.shift)
        if action is not None:
            # Don't hide the window from inside its own render.
            cron.after("0ms", action)

        area = ui.available_rect_before_wrap()
        heading = chip.label if chip is not None else "All windows"
        # The close button, for the mouse: top right, in line with the search field's edge.
        close_rect = egui.Rect.from_min_size(
            egui.Pos2(area.max.x - PADDING - CLOSE_BUTTON, area.min.y + (HEADER_HEIGHT - CLOSE_BUTTON) / 2),
            egui.Vec2(CLOSE_BUTTON, CLOSE_BUTTON),
        )
        if self._draw_close_button(ui, painter, close_rect):
            cron.after("0ms", self.cancel)
        header_right = close_rect.min.x - PADDING
        if mode in APP_MODES or placement is None:
            # The layout switch of every view: icons (or tiles) or details. Not while
            # placing windows, which needs the tiles.
            label = "Icons" if details else "Details"
            galley = painter.layout_no_wrap(label, egui.FontId.proportional(13.0), TEXT)
            pill = egui.Rect.from_min_size(
                egui.Pos2(header_right - galley.size().x - 16, area.min.y + (HEADER_HEIGHT - 22) / 2), egui.Vec2(galley.size().x + 16, 22)
            )
            response = hit(ui, pill, "layout")
            describe(response, egui.WidgetType.Button, label)
            painter.rect_filled(pill, 5, TILE_HOVER if response.hovered() else TILE)
            painter.rect_stroke(pill, 5, egui.Stroke(1.0, BORDER), egui.StrokeKind.Inside)
            painter.galley(egui.Pos2(pill.min.x + 8, pill.min.y + (22 - galley.size().y) / 2), galley, TEXT)
            if response.hovered():
                response.on_hover_text("Switch between icons and details (Ctrl+D)")
            if response.clicked():
                if mode == "launcher":
                    cron.after("0ms", lambda: self.set_launcher_details(None))
                elif mode == "apps":
                    cron.after("0ms", lambda: self.set_apps_details(not self.apps_details))
                else:
                    cron.after("0ms", lambda: self.show_window_details(not self.window_details))
            header_right = pill.min.x - PADDING
        if mode in ("windows", "apps") and placement is None:
            # Over to the other view, unfiltered: windows <-> apps.
            label = "Apps" if mode == "windows" else "Windows"
            galley = painter.layout_no_wrap(label, egui.FontId.proportional(13.0), TEXT)
            pill = egui.Rect.from_min_size(
                egui.Pos2(header_right - galley.size().x - 16, area.min.y + (HEADER_HEIGHT - 22) / 2), egui.Vec2(galley.size().x + 16, 22)
            )
            response = hit(ui, pill, "view")
            describe(response, egui.WidgetType.Button, f"Show {label.lower()}")
            painter.rect_filled(pill, 5, TILE_HOVER if response.hovered() else TILE)
            painter.rect_stroke(pill, 5, egui.Stroke(1.0, BORDER), egui.StrokeKind.Inside)
            painter.galley(egui.Pos2(pill.min.x + 8, pill.min.y + (22 - galley.size().y) / 2), galley, TEXT)
            if response.hovered():
                response.on_hover_text(f"Show {label.lower()}, without filters (Ctrl+Tab)")
            if response.clicked():
                cron.after("0ms", self.switch_view)
            header_right = pill.min.x - PADDING
        header_action = None
        if placement is None and marked:
            # The marked windows' bar, instead of the hint.
            visible = {h for e in entries for h in tile_hwnds(e)}
            hidden = sum(1 for h in marked if h not in visible)
            header_action = self._draw_mark_bar(ui, painter, area, len(marked), hidden, show_screens, header_right)
        elif placement is not None:
            text = (
                f"Placing {slot_label(placement.layout)}: {slot_label(placement.slot)} "
                f"({placement.index + 1} of {len(placement.slots)}). Say a number, skip, or cancel"
            )
        elif mode == "launcher":
            text = f"{'App launcher' if chip is None else heading}: type to search, a number or Enter focuses or launches, \"launch new\" a number, \"jump\" a letter or Alt+letter" + (", \"sort by\" a column" if details else "")
        elif mode == "apps" and details:
            text = f"{'Apps' if chip is None else heading}: type to search, say a number or Enter to focus, \"sort by\" a column, Ctrl+D for icons"
        elif mode == "apps":
            text = f"{'Apps' if chip is None else heading}: type to search, say a number or Enter to focus, Down for its windows"
        elif details:
            text = f"{heading}: type to search, say a number or Enter to focus, \"sort by\" a column, Ctrl+D switches views"
        else:
            text = f"{heading}: type to search, say a number, click a window, or use the arrow keys and Enter"
        if not (placement is None and marked):
            painter.text(
                egui.Pos2(area.min.x + PADDING, area.min.y + HEADER_HEIGHT / 2),
                egui.Align2.LEFT_CENTER,
                elide(text, header_right - area.min.x - PADDING, 15.0),
                egui.FontId.proportional(15.0),
                SELECTED if placement is not None else TEXT,
            )
        if header_action is not None:
            cron.after("0ms", header_action)
        field = egui.Rect.from_min_max(
            egui.Pos2(area.min.x + PADDING, area.min.y + HEADER_HEIGHT),
            egui.Pos2(area.max.x - PADDING, area.min.y + HEADER_HEIGHT + SEARCH_HEIGHT - PADDING),
        )
        if placement is not None:
            minimap = egui.Rect.from_min_max(
                egui.Pos2(field.max.x - MINIMAP_WIDTH, field.min.y), field.max
            )
            field = egui.Rect.from_min_max(field.min, egui.Pos2(minimap.min.x - PADDING, field.max.y))
            self._draw_minimap(painter, minimap, placement)
        self._draw_search(ui, painter, field, chip, query)
        show_desktops = len(desktops) > 1

        # Everything below the header and search field scrolls; tiles are clipped to
        # this viewport, so the search field stays put.
        viewport = egui.Rect.from_min_max(
            egui.Pos2(area.min.x, area.min.y + HEADER_HEIGHT + SEARCH_HEIGHT + (COLUMN_HEADER_HEIGHT if details else 0)), area.max
        )
        gap = PADDING if previews else ROW_GAP
        sections = launcher_sections(entries, running_count) if running_count is not None else []
        letter_at = launcher_letters(entries, running_count) if running_count is not None else {}
        # The A-Z index fits the default order, or sorting by application.
        index_letters = set(letter_at.values()) if sort_column in (None, "name") else set()
        if sort_column not in (None, "name"):
            letter_at = {}
        # The launcher keeps room for its A-Z index on the right.
        index_w = INDEX_WIDTH + 6 if index_letters else 0.0
        cell_w = (viewport.width() - 2 * PADDING - index_w) / cols
        if details:
            cell_h = DETAIL_ROW_HEIGHT + ROW_GAP
        elif mode in APP_MODES:
            cell_h = cell_w
        elif previews:
            cell_h = (cell_w - PADDING) / TILE_ASPECT + LABEL_HEIGHT + PADDING
        else:
            cell_h = ROW_HEIGHT + ROW_GAP
        layout = tile_layout(len(entries), cols, sections)

        def tile_top(i: int) -> float:
            """Tile `i`'s top within the scrolled content."""
            _col, row, headings = layout[i]
            return row * cell_h + headings * SECTION_HEIGHT

        with self.lock:
            self.layout, self.sections = layout, sections
            self.page_rows = max(1, int(viewport.height() // max(cell_h, 1)) - 1)
            scroll_to, self.scroll_to = self.scroll_to, None

        content_h = PADDING + (tile_top(len(entries) - 1) + cell_h if entries else 0)
        max_scroll = max(content_h - viewport.height(), 0.0)

        scroll = self.scroll - wheel
        if scroll_to is not None and 0 <= scroll_to < len(entries):
            # A letter jump: its row at the top.
            scroll = tile_top(scroll_to) - PADDING / 2
        elif reveal and 0 <= current < len(entries):
            # With its heading, if it has one.
            top = tile_top(current) - (SECTION_HEIGHT if layout[current][2] else 0)
            bottom = top + cell_h + PADDING
            if top < scroll:
                scroll = top
            elif bottom > scroll + viewport.height():
                scroll = bottom - viewport.height()
        scroll = max(0.0, min(scroll, max_scroll))
        self.scroll = scroll

        columns = (
            detail_columns(cell_w - PADDING, show_screens, WINDOW_DETAIL_COLUMNS if window_rows else DETAIL_COLUMNS) if details else []
        )

        clipped = ui.painter_at(viewport)
        view_px = to_pixels(viewport, ppp)
        selected = None
        mark_click = None
        close_click = None
        shown = set()
        # The menu goes where it was opened, or for keyboard and voice at its tile; it's
        # sized now so the thumbnails it covers can be hidden (DWM draws over it).
        menu_rect = None
        if menu is not None:
            items = self._menu_items(menu_entry, menu.page)
            anchor = menu.pos
            if anchor is None:
                # The marked windows' menu opens at the selected tile.
                index = entries.index(menu_entry) if menu_entry is not None else max(0, min(current, len(entries) - 1))
                col = layout[index][0]
                anchor = egui.Pos2(
                    viewport.min.x + PADDING + col * cell_w + 40,
                    viewport.min.y + PADDING + tile_top(index) - scroll + 20,
                )
            height = sum(menu_row_height(item) for item in items) + 2 * MENU_PADDING
            menu_w = JUMP_MENU_WIDTH if menu.page.startswith("jump") else MENU_WIDTH
            if height > area.height() or menu_w > area.width():
                # Too big for the window (a few apps, or a long jump list page): the
                # window grows until the menu closes, so it's never cut off.
                extra = (max(0.0, height - area.height()) + PADDING, max(0.0, menu_w - area.width()) + PADDING)
                cron.after("0ms", lambda extra=extra: self._grow_for_menu(*extra))
            x = min(max(anchor.x, area.min.x), area.max.x - menu_w)
            y = min(max(anchor.y, area.min.y), area.max.y - height)
            menu_rect = egui.Rect.from_min_size(egui.Pos2(x, y), egui.Vec2(menu_w, height))
        menu_px = to_pixels(menu_rect, ppp) if menu_rect is not None else None

        if not entries:
            painter.text(
                egui.Pos2(viewport.center().x, viewport.min.y + 3 * PADDING),
                egui.Align2.CENTER_TOP,
                "No matching windows",
                egui.FontId.proportional(15.0),
                DIM_TEXT,
            )

        if sections:
            # The launcher's section headings.
            for first, label in sections:
                y = viewport.min.y + PADDING + tile_top(first) - SECTION_HEIGHT / 2 - scroll
                if viewport.min.y - SECTION_HEIGHT < y < viewport.max.y:
                    clipped.text(
                        egui.Pos2(viewport.min.x + PADDING + 4, y), egui.Align2.LEFT_CENTER, label, egui.FontId.proportional(15.0), DIM_TEXT
                    )

        for i, entry in enumerate(entries):
            col = layout[i][0]
            tile = egui.Rect.from_min_size(
                egui.Pos2(
                    viewport.min.x + PADDING + col * cell_w,
                    viewport.min.y + PADDING + tile_top(i) - scroll,
                ),
                egui.Vec2(cell_w - PADDING, cell_h - gap),
            )
            thumbnail = thumbnails.get(entry.hwnd)
            if not tile.intersects(viewport):
                if thumbnail is not None:
                    thumbnail.hide()
                continue

            # Each tile's close button, Alt+Tab style. It sits on the tile, which gets
            # egui's hover and clicks, so the pointer's position decides between them.
            # Not while placing, where clicks pick windows.
            close_rect = self._tile_close_rect(tile, "details" if details else mode, previews)
            has_close = menu is None and placement is None and viewport.contains_rect(close_rect) and bool(tile_hwnds(entry))
            # The close button's own area comes first, under the tile's, so it is its own
            # UIA element (invoked by UI Automation) while the tile still gets the mouse.
            close_response = hit(ui, close_rect, f"tile-close:{entry.hwnd}") if has_close else None
            if close_response is not None:
                describe(close_response, egui.WidgetType.Button, f"Close {entry.title}")
            response = hit(ui, tile.intersect(viewport), f"tile:{entry.hwnd}")
            describe(response, egui.WidgetType.SelectableLabel, f"{i + 1} {self._tile_name(entry, mode)}", True, i == current)
            close_hovered = (
                has_close and response.hovered() and pointer_pos is not None and close_rect.contains(pointer_pos)
            )
            hovered = response.hovered() and not close_hovered
            if hovered and i != current and pointer_moving and pointer_moving_now and menu is None:
                # The mouse moves the selection too, but only while it actually moves
                # (not when tiles scroll under a resting pointer, e.g. after a letter
                # jump), and not while a menu is open for the selected tile.
                with self.lock:
                    self.selected = current = i
            # (An installed app in the launcher has no windows to mark.)
            is_marked = bool(marked) and bool(tile_hwnds(entry)) and all(h in marked for h in tile_hwnds(entry))
            if is_marked:
                fill = MARKED_FILL
            else:
                fill = TILE_HOVER if (hovered or close_hovered) and menu is None else TILE
            clipped.rect_filled(tile, 6, fill)
            if i == current:
                clipped.rect_stroke(
                    tile, 6, egui.Stroke(SELECTED_WIDTH, SELECTED), egui.StrokeKind.Inside
                )
            elif is_marked:
                clipped.rect_stroke(tile, 6, egui.Stroke(2.0, MARKED), egui.StrokeKind.Inside)
            else:
                clipped.rect_stroke(tile, 6, egui.Stroke(1.0, BORDER), egui.StrokeKind.Inside)

            badges = []
            if entry.hwnd in placed:
                badges.append((f"placed: {slot_label(placed[entry.hwnd])}", SELECTED))
            if show_desktops and entry.desktop_number:
                desktop = next((d for d in desktops if d.number == entry.desktop_number), None)
                is_current = entry.desktop_key == current_desktop
                badges.append((desktop.label() if desktop else str(entry.desktop_number), CURRENT_DESKTOP if is_current else BORDER))
            if show_screens and entry.screen_number and mode not in APP_MODES:
                badges.append((f"Screen {entry.screen_number}", SCREEN_BADGE))
            if details:
                self._draw_detail_row(
                    ui, clipped, entry, i, tile, columns, letter_at.get(i), current_desktop, show_desktops, is_marked
                )
            elif mode in APP_MODES:
                if show_desktops and entry.desktop_numbers:
                    here = current_desktop is not None and any(w.desktop_key == current_desktop for w in entry.windows)
                    numbers = ", ".join(str(n) for n in entry.desktop_numbers)
                    label = f"Desktop{'s' if len(entry.desktop_numbers) > 1 else ''} {numbers}"
                    badges.append((label, CURRENT_DESKTOP if here else BORDER))
                self._draw_app_tile(ui, clipped, entry, i, tile, badges, is_marked, launcher=mode == "launcher", letter=letter_at.get(i))
            elif previews:
                shown.add(entry.hwnd)
                self._draw_tile(ui, clipped, entry, i, tile, thumbnail, view_px, ppp, badges, menu_px, is_marked)
            else:
                self._draw_row(ui, clipped, entry, i, tile, badges, is_marked)

            if has_close and (hovered or close_hovered or i == current):
                self._paint_close(clipped, close_rect, close_hovered)
                if close_hovered:
                    response.on_hover_text(
                        f"Close all {entry.app_name} windows" if mode in APP_MODES else "Close window"
                    )
            if (close_hovered and response.clicked()) or (close_response is not None and close_response.clicked()):
                # Just this window (or app), even when others are marked.
                close_click = i + 1
            elif menu is None and response.clicked():
                if ctrl_down or shift_down:
                    # Ctrl+click toggles a mark, Shift+click marks a range; a plain
                    # click still focuses the window.
                    with self.lock:
                        self.selected = i
                    mark_click = (self.mark, [i + 1]) if ctrl_down else (self.mark_to, i + 1)
                else:
                    selected = i + 1
            elif response.secondary_clicked():
                with self.lock:
                    self.selected = i
                    # On a marked tile: the marked windows' menu.
                    self.menu = Menu(None, pointer_pos, marked=True) if is_marked else Menu(entry.hwnd, pointer_pos)
                ui.ctx().request_repaint()
                cron.after("0ms", self._update_tags)

        # Windows filtered out by the search keep their thumbnail registered, hidden.
        for hwnd, thumbnail in thumbnails.items():
            if hwnd not in shown:
                thumbnail.hide()

        if details:
            # The column headings, pinned above the rows; a click sorts by that column.
            # Drawn after the rows, on an opaque band, so that rows scrolled up under
            # them never show through (or take their clicks).
            y0 = viewport.min.y - COLUMN_HEADER_HEIGHT
            painter.rect_filled(
                egui.Rect.from_min_max(egui.Pos2(area.min.x, y0), egui.Pos2(area.max.x, viewport.min.y)), 0, BACKGROUND
            )
            for key, heading_text, x, w in columns:
                if not heading_text:
                    continue
                cell = egui.Rect.from_min_size(egui.Pos2(viewport.min.x + PADDING + x, y0), egui.Vec2(w, COLUMN_HEADER_HEIGHT))
                if key in SORTABLE:
                    response = hit(ui, cell, "sort:" + key)
                    describe(response, egui.WidgetType.Button, f"Sort by {heading_text}")
                    if response.hovered():
                        painter.rect_filled(cell, 4, TILE_HOVER)
                    if response.clicked():
                        cron.after("0ms", lambda key=key: self.sort_launcher(key))
                text_rect = painter.text(
                    egui.Pos2(cell.min.x + 6, cell.center().y), egui.Align2.LEFT_CENTER, heading_text, egui.FontId.proportional(13.0), DIM_TEXT
                )
                if sort_column == key:
                    # The sort direction as a small chevron (the font has no triangles).
                    cx, cy, r = text_rect.max.x + 9, cell.center().y, 3.5
                    dy = r if sort_reverse else -r
                    stroke = egui.Stroke(1.5, DIM_TEXT)
                    painter.line_segment(egui.Pos2(cx - r, cy - dy / 2), egui.Pos2(cx, cy + dy / 2), stroke)
                    painter.line_segment(egui.Pos2(cx, cy + dy / 2), egui.Pos2(cx + r, cy - dy / 2), stroke)
            painter.line_segment(
                egui.Pos2(viewport.min.x + PADDING, viewport.min.y - 1), egui.Pos2(viewport.max.x - PADDING, viewport.min.y - 1), egui.Stroke(1.0, BORDER)
            )

        if index_letters:
            jump_letter = self._draw_index(ui, painter, viewport, index_letters, entries, current, running_count)
            if jump_letter is not None:
                cron.after("0ms", lambda: self.jump(jump_letter))

        if max_scroll > 0:
            track = egui.Rect.from_min_max(
                egui.Pos2(viewport.max.x - PADDING / 2 - SCROLLBAR_WIDTH / 2, viewport.min.y + PADDING),
                egui.Pos2(viewport.max.x - PADDING / 2 + SCROLLBAR_WIDTH / 2, viewport.max.y - PADDING),
            )
            bar_h = max(track.height() * viewport.height() / content_h, 20.0)
            bar_top = track.min.y + (track.height() - bar_h) * scroll / max_scroll
            painter.rect_filled(
                egui.Rect.from_min_size(
                    egui.Pos2(track.min.x, bar_top), egui.Vec2(SCROLLBAR_WIDTH, bar_h)
                ),
                2,
                BORDER,
            )

        if menu_rect is not None:
            pick = self._draw_menu(ui, painter, menu, items, menu_rect, pointer_moving_now, pointer_pos)
            if pick is not None:
                cron.after("0ms", lambda: self._pick(menu, pick))
            elif primary_clicked and pointer_pos is not None and not menu_rect.contains(pointer_pos):
                # A click elsewhere closes the menu (and doesn't pick a tile).
                cron.after("0ms", self.close_menu)

        if mark_click is not None:
            cron.after("0ms", lambda: mark_click[0](mark_click[1]))
        if close_click is not None:
            cron.after("0ms", lambda: self.close_windows([close_click]))
        if selected is not None:
            # Don't hide the window from inside its own render.
            cron.after("0ms", lambda: self.select(selected))

    def _draw_index(self, ui, painter, viewport, letters: set, entries: list, current: int, running: int):
        """The launcher's A-Z index down the right edge: letters with apps are clickable,
        the selected app's letter is highlighted. Returns a clicked letter."""
        top = viewport.min.y + PADDING
        height = min(22.0, (viewport.height() - 2 * PADDING) / len(INDEX_LETTERS))
        x = viewport.max.x - PADDING / 2 - SCROLLBAR_WIDTH - INDEX_WIDTH / 2 - 2
        here = index_letter(entries[current].title) if running <= current < len(entries) else None
        clicked = None
        font = egui.FontId.proportional(12.0)
        for n, letter in enumerate(INDEX_LETTERS):
            rect = egui.Rect.from_center_size(egui.Pos2(x, top + (n + 0.5) * height), egui.Vec2(INDEX_WIDTH, height))
            enabled = letter in letters
            color = DIM_TEXT
            if enabled:
                response = hit(ui, rect, "letter:" + letter)
                describe(response, egui.WidgetType.Button, f"Jump to {letter}")
                if response.hovered():
                    painter.rect_filled(rect, 4, TILE_HOVER)
                if response.clicked():
                    clicked = letter
                color = SELECTED if letter == here else TEXT
            else:
                color = egui.Color32.from_rgb(80, 80, 88)
            painter.text(rect.center(), egui.Align2.CENTER_CENTER, letter, font, color)
        return clicked

    def _draw_app_tile(
        self,
        ui: egui.Ui,
        painter: egui.Painter,
        group: AppGroup,
        i: int,
        tile: egui.Rect,
        badges: list,
        marked: bool = False,
        launcher: bool = False,
        letter: str | None = None,
    ):
        """An apps-view tile: number, large icon, app name, window count, badges. In the
        launcher, running apps get a green dot and their window count even with one, and
        the first installed app of each letter a letter marker."""
        if letter:
            pill = egui.Rect.from_center_size(egui.Pos2(tile.max.x - 18, tile.min.y + 14), egui.Vec2(22, 20))
            painter.rect_filled(pill, 5, CHIP)
            painter.text(pill.center(), egui.Align2.CENTER_CENTER, letter, egui.FontId.proportional(14.0), WHITE)
        number = painter.text(
            egui.Pos2(tile.min.x + 8, tile.min.y + 12),
            egui.Align2.LEFT_CENTER,
            str(i + 1),
            egui.FontId.proportional(14.0),
            DIM_TEXT,
        )
        if marked:
            self._draw_check(painter, egui.Pos2(number.max.x + 12, tile.min.y + 12))
        count = len(group.windows)
        if count > 1 or (launcher and count):
            text = painter.text(
                egui.Pos2(tile.max.x - 12 - TILE_CLOSE, tile.min.y + 12),
                egui.Align2.RIGHT_CENTER,
                f"{count} window{'s' if count > 1 else ''}",
                egui.FontId.proportional(12.0),
                DIM_TEXT,
            )
            if launcher:
                painter.circle_filled(egui.Pos2(text.min.x - 8, tile.min.y + 12), 4.0, RUNNING_DOT)
        size = min(APP_ICON, tile.width() - 24, tile.height() - 72)
        center_x = tile.center().x
        top = tile.min.y + 24
        texture = self._texture(ui, group)
        if texture is not None and size > 0:
            rect = egui.Rect.from_min_size(egui.Pos2(center_x - size / 2, top), egui.Vec2(size, size))
            uv = egui.Rect.from_min_max(egui.Pos2(0.0, 0.0), egui.Pos2(1.0, 1.0))
            painter.image(texture.id(), rect, uv, WHITE if not group.minimized else DIM_TEXT)
        painter.text(
            egui.Pos2(center_x, top + max(size, 0) + 14),
            egui.Align2.CENTER_CENTER,
            elide(group.title, tile.width() - 12, 14.0),
            egui.FontId.proportional(14.0),
            TEXT,
        )
        if badges:
            # Centered along the bottom.
            width = sum(text_points(text, 12.0) + 18 for text, _color in badges)
            self._draw_badges(painter, badges, center_x + width / 2, tile.max.y - 14)

    def _draw_menu(
        self, ui: egui.Ui, painter: egui.Painter, menu: Menu, items: list, rect: egui.Rect, hover: bool, pointer=None
    ):
        """Draw the menu; returns the item clicked this frame, if any. A click on a row's
        icon button returns that button's action as an item that keeps the menu open."""
        painter.rect_filled(rect, 8, MENU_BACKGROUND)
        painter.rect_stroke(rect, 8, egui.Stroke(1.0, MENU_BORDER), egui.StrokeKind.Inside)
        font = egui.FontId.proportional(14.0)
        picked = None
        numbers = menu_numbers(items)
        # The icon column only on pages with icons (jump lists).
        label_x = MENU_LABEL_X if any(item.icon is not None for item in items) else MENU_LABEL_X - MENU_ICON - 4
        top = rect.min.y + MENU_PADDING
        for i, item in enumerate(items):
            row = egui.Rect.from_min_size(
                egui.Pos2(rect.min.x + MENU_PADDING, top), egui.Vec2(rect.width() - 2 * MENU_PADDING, menu_row_height(item))
            )
            top += row.height()
            if item.kind == "separator":
                y = row.center().y
                painter.line_segment(egui.Pos2(rect.min.x, y), egui.Pos2(rect.max.x, y), egui.Stroke(1.0, MENU_BORDER))
                continue
            if item.kind == "heading":
                # Like the Start menu's: small grey text, further left than the items.
                painter.text(
                    egui.Pos2(row.min.x + 10, row.center().y + 2),
                    egui.Align2.LEFT_CENTER,
                    elide(item.label, row.width() - 20, 13.0),
                    egui.FontId.proportional(13.0),
                    DIM_TEXT,
                )
                continue
            # Icon buttons at the row's end, shown on the highlighted row.
            button_rects = []
            right = row.max.x - 4
            for kind, action in reversed(item.buttons):
                button = egui.Rect.from_min_size(
                    egui.Pos2(right - MENU_BUTTON, row.center().y - MENU_BUTTON / 2), egui.Vec2(MENU_BUTTON, MENU_BUTTON)
                )
                button_rects.append((kind, action, button))
                right = button.min.x - 4
            # The buttons' own areas first, under the row's (as with tiles' close buttons):
            # UIA elements of their own, while the pointer decides for the mouse.
            invoked = None
            for kind, action, button in button_rects:
                bresp = hit(ui, button, f"menu-button:{menu.page}:{i}:{kind}")
                describe(bresp, egui.WidgetType.Button, f"{MENU_BUTTON_TIPS.get(kind, kind)}: {item.label}")
                if bresp.clicked():
                    invoked = (kind, action)
            response = hit(ui, row, f"menu:{menu.page}:{i}")
            describe(response, egui.WidgetType.Button, item.label[:-3] if item.label.endswith("  >") else item.label, item.enabled)
            if hover and response.hovered() and item.enabled and menu.highlight != i:
                menu.highlight = i
            if menu.highlight == i and item.enabled:
                painter.rect_filled(row, 4, MENU_HOVER)
            on_button = None
            for kind, action, button in button_rects:
                over = response.hovered() and pointer is not None and button.contains(pointer)
                if over:
                    on_button = (kind, action)
                    response.on_hover_text(MENU_BUTTON_TIPS.get(kind, kind))
                if menu.highlight == i or over:
                    self._paint_menu_button(painter, button, kind, over)
            # Numbered for voice and digit keys (the number picks it while the menu is
            # open, instead of acting on tiles), small and grey in the gutter.
            if numbers[i]:
                painter.text(
                    egui.Pos2(row.min.x + 22, row.center().y), egui.Align2.RIGHT_CENTER, str(numbers[i]), egui.FontId.proportional(12.0), DIM_TEXT
                )
            texture = self._menu_icon(ui, item.icon) if item.icon is not None else None
            if texture is not None:
                icon_rect = egui.Rect.from_min_size(
                    egui.Pos2(row.min.x + 28, row.center().y - MENU_ICON / 2), egui.Vec2(MENU_ICON, MENU_ICON)
                )
                painter.image(texture.id(), icon_rect, egui.Rect.from_min_max(egui.Pos2(0.0, 0.0), egui.Pos2(1.0, 1.0)), WHITE)
            label = item.label
            if label.endswith("  >"):
                # A submenu: its chevron at the row's end, as Windows menus have it.
                label = label[:-3]
                painter.text(egui.Pos2(right - 6, row.center().y), egui.Align2.RIGHT_CENTER, "›", egui.FontId.proportional(18.0), DIM_TEXT)
            painter.text(
                egui.Pos2(row.min.x + label_x, row.center().y),
                egui.Align2.LEFT_CENTER,
                elide(label, right - row.min.x - label_x - 20, 14.0),
                font,
                TEXT if item.enabled else DIM_TEXT,
            )
            if invoked is not None:
                picked = MenuItem(invoked[0], invoked[1], keep_open=True)
            elif response.clicked() and on_button is not None:
                picked = MenuItem(on_button[0], on_button[1], keep_open=True)
            elif response.clicked() and item.enabled:
                picked = item
        return picked

    def _draw_detail_row(self, ui, painter, entry, i, row, columns, letter, current_desktop, show_desktops, marked):
        """A row of the launcher's details table."""
        center_y = row.center().y
        font = egui.FontId.proportional(13.0)
        windows = getattr(entry, "windows", [])
        for key, _heading, x, w in columns:
            left = row.min.x + x + 6
            width = w - 12
            if key == "number":
                painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, str(i + 1), egui.FontId.proportional(14.0), DIM_TEXT)
                if marked:
                    self._draw_check(painter, egui.Pos2(left + 26, center_y), radius=6.0)
            elif key == "icon":
                texture = self._texture(ui, entry)
                if texture is not None:
                    rect = egui.Rect.from_min_size(egui.Pos2(left - 4, center_y - 11), egui.Vec2(22, 22))
                    uv = egui.Rect.from_min_max(egui.Pos2(0.0, 0.0), egui.Pos2(1.0, 1.0))
                    painter.image(texture.id(), rect, uv, WHITE)
            elif key == "name":
                # (No letter pill here: the A-Z index on the right shows where you are.)
                # A window row's Application is its app; the launcher's rows are apps.
                name = entry.app_name if isinstance(entry, Entry) else entry.title
                painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, elide(name, width, 14.0), egui.FontId.proportional(14.0), TEXT)
            elif key == "title":
                painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, elide(entry.title, width, 14.0), egui.FontId.proportional(14.0), TEXT)
            elif key == "state":
                state = window_state(entry)
                painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, state, font, DIM_TEXT if state == "Normal" else TEXT)
            elif key == "running":
                if windows:
                    painter.circle_filled(egui.Pos2(left + 4, center_y), 4.0, RUNNING_DOT)
                    painter.text(
                        egui.Pos2(left + 14, center_y), egui.Align2.LEFT_CENTER, f"{len(windows)} window{'s' if len(windows) > 1 else ''}", font, TEXT
                    )
            elif key == "spoken":
                forms = self._spoken_forms(entry)
                if forms:
                    painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, elide(", ".join(forms[:2]), width, 13.0), font, TEXT)
            elif key == "desktop":
                numbers = getattr(entry, "desktop_numbers", None) or []
                if isinstance(entry, Entry):
                    numbers = [entry.desktop_number] if entry.desktop_number else []
                    windows = [entry]
                if numbers and show_desktops:
                    here = current_desktop is not None and any(w.desktop_key == current_desktop for w in windows)
                    painter.text(
                        egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, ", ".join(str(n) for n in numbers), font, CURRENT_DESKTOP if here else TEXT
                    )
                elif numbers:
                    painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, ", ".join(str(n) for n in numbers), font, DIM_TEXT)
            elif key == "screen":
                numbers = getattr(entry, "screen_numbers", None) or []
                if isinstance(entry, Entry):
                    numbers = [entry.screen_number] if entry.screen_number else []
                if numbers:
                    painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, ", ".join(str(n) for n in numbers), font, TEXT)


    def _paint_menu_button(self, painter: egui.Painter, rect: egui.Rect, kind: str, hovered: bool):
        """A menu row's icon: a pushpin (pin), a crossed-out pushpin (unpin), an × (remove)."""
        if hovered:
            painter.rect_filled(rect, 4, CLOSE_HOVER if kind == "remove" else CHIP)
        color = WHITE if hovered else TEXT
        stroke = egui.Stroke(1.6, color)
        c = rect.center()
        if kind == "remove":
            r = rect.width() * 0.22
            painter.line_segment(egui.Pos2(c.x - r, c.y - r), egui.Pos2(c.x + r, c.y + r), stroke)
            painter.line_segment(egui.Pos2(c.x - r, c.y + r), egui.Pos2(c.x + r, c.y - r), stroke)
            return
        # A pushpin: round head, a bar, and the needle.
        painter.circle_filled(egui.Pos2(c.x, c.y - 4), 3.2, color)
        painter.line_segment(egui.Pos2(c.x - 4, c.y), egui.Pos2(c.x + 4, c.y), stroke)
        painter.line_segment(egui.Pos2(c.x, c.y), egui.Pos2(c.x, c.y + 6), stroke)
        if kind == "unpin":
            painter.line_segment(egui.Pos2(c.x - 6, c.y + 6), egui.Pos2(c.x + 6, c.y - 7), egui.Stroke(1.8, CLOSE_HOVER if not hovered else WHITE))

    def _draw_tile(
        self,
        ui: egui.Ui,
        painter: egui.Painter,
        entry: Entry,
        i: int,
        tile: egui.Rect,
        thumbnail: "dwm.Thumbnail | None",
        view_px: tuple[int, int, int, int],
        ppp: float,
        badges: list,
        cover: tuple[int, int, int, int] | None = None,
        marked: bool = False,
    ):
        """A grid tile: the live thumbnail (or icon) with the number and title below;
        a marked one has a check before the number (DWM draws over the thumbnail area)."""
        label_y = tile.max.y - LABEL_HEIGHT / 2 - 2
        # Room for the close button at the end.
        right = self._draw_badges(painter, badges, tile.max.x - 10 - TILE_CLOSE, label_y)
        left = tile.min.x + 6
        if marked:
            self._draw_check(painter, egui.Pos2(left + 7, label_y))
            left += 18
        label = f"{i + 1}  {entry.title}"
        painter.text(
            egui.Pos2(left, label_y),
            egui.Align2.LEFT_CENTER,
            elide(label, right - left - 6, 13.0),
            egui.FontId.proportional(13.0),
            TEXT,
        )

        # The thumbnail area; shown underneath DWM's thumbnail, so it only shows
        # through while the thumbnail is not registered or has no content.
        thumb = egui.Rect.from_min_max(
            egui.Pos2(tile.min.x + 6, tile.min.y + 6),
            egui.Pos2(tile.max.x - 6, tile.max.y - LABEL_HEIGHT - 4),
        )
        if entry.iconic:
            self._draw_icon(ui, painter, entry, thumb)
        else:
            painter.text(
                thumb.center(),
                egui.Align2.CENTER_CENTER,
                elide(entry.app_name, thumb.width(), 14.0),
                egui.FontId.proportional(14.0),
                DIM_TEXT,
            )

        if thumbnail is not None:
            box = to_pixels(thumb, ppp)
            dest = fit(*thumbnail.source_size(), box)
            if cover is not None and dwm.intersect(dest, cover):
                # Under the menu: DWM would draw on top of it. Back once the menu closes.
                thumbnail.hide()
            else:
                # Clipped to the viewport: DWM would otherwise draw over the header.
                thumbnail.place(dest, view_px)

    def _draw_row(
        self, ui: egui.Ui, painter: egui.Painter, entry: Entry, i: int, row: egui.Rect, badges: list, marked: bool = False
    ):
        """A list row: number, small icon, window title and, dimmer, the app name; a
        marked row has a check on the icon's corner."""
        center_y = row.center().y
        x = row.min.x + 10
        painter.text(
            egui.Pos2(x, center_y),
            egui.Align2.LEFT_CENTER,
            str(i + 1),
            egui.FontId.proportional(14.0),
            DIM_TEXT,
        )
        x += NUMBER_WIDTH
        texture = self._texture(ui, entry)
        if texture is not None:
            rect = egui.Rect.from_min_size(
                egui.Pos2(x, center_y - ROW_ICON / 2), egui.Vec2(ROW_ICON, ROW_ICON)
            )
            uv = egui.Rect.from_min_max(egui.Pos2(0.0, 0.0), egui.Pos2(1.0, 1.0))
            painter.image(texture.id(), rect, uv, WHITE)
        if marked:
            self._draw_check(painter, egui.Pos2(x + ROW_ICON - 2, center_y + ROW_ICON / 2 - 4), radius=6.0)
        x += ROW_ICON + 10

        app_label = entry.app_label()
        # Room for the close button at the end.
        right = self._draw_badges(painter, badges, row.max.x - 14 - TILE_CLOSE, center_y)
        app_w = min(text_points(app_label, 13.0), row.width() * 0.35)
        painter.text(
            egui.Pos2(right, center_y),
            egui.Align2.RIGHT_CENTER,
            elide(app_label, app_w, 13.0),
            egui.FontId.proportional(13.0),
            DIM_TEXT,
        )
        painter.text(
            egui.Pos2(x, center_y),
            egui.Align2.LEFT_CENTER,
            elide(entry.title, right - app_w - 24 - x, 14.0),
            egui.FontId.proportional(14.0),
            TEXT,
        )

    def _draw_check(self, painter: egui.Painter, center: egui.Pos2, radius: float = 7.0):
        """The marked tiles' check: a tick on a filled circle."""
        painter.circle_filled(center, radius, MARKED)
        stroke = egui.Stroke(1.8, WHITE)
        a = egui.Pos2(center.x - radius * 0.5, center.y)
        b = egui.Pos2(center.x - radius * 0.12, center.y + radius * 0.4)
        c = egui.Pos2(center.x + radius * 0.5, center.y - radius * 0.38)
        painter.line_segment(a, b, stroke)
        painter.line_segment(b, c, stroke)

    def _tile_name(self, entry, mode: str) -> str:
        """A tile's accessible name: its title, and what it is (apps: windows, or not running)."""
        if mode in APP_MODES:
            count = len(getattr(entry, "windows", []))
            return f"{entry.title}, {count} window{'s' if count != 1 else ''}" if count else f"{entry.title}, not running"
        app_name = getattr(entry, "app_name", "")
        return f"{entry.title} ({app_name})" if app_name and app_name.lower() not in entry.title.lower() else entry.title

    def _draw_close_button(self, ui: egui.Ui, painter: egui.Painter, rect: egui.Rect) -> bool:
        """An × that closes the switcher, like Escape; returns whether it was clicked."""
        response = hit(ui, rect, "close")
        describe(response, egui.WidgetType.Button, "Close switcher")
        if response.hovered():
            response.on_hover_text("Close (Esc)")
        self._paint_close(painter, rect, response.hovered())
        return response.clicked()

    def _tile_close_rect(self, tile: egui.Rect, mode: str, previews: bool) -> egui.Rect:
        """Where a tile's close button goes: the top right of an app tile, the right end
        of a list row, and in the grid the right end of the label row (DWM draws the
        thumbnail over the rest of the tile)."""
        if mode in APP_MODES:
            center = egui.Pos2(tile.max.x - 6 - TILE_CLOSE / 2, tile.min.y + 12)
        elif previews:
            center = egui.Pos2(tile.max.x - 6 - TILE_CLOSE / 2, tile.max.y - LABEL_HEIGHT / 2 - 2)
        else:
            center = egui.Pos2(tile.max.x - 8 - TILE_CLOSE / 2, tile.center().y)
        return egui.Rect.from_center_size(center, egui.Vec2(TILE_CLOSE, TILE_CLOSE))

    def _paint_close(self, painter: egui.Painter, rect: egui.Rect, hovered: bool):
        """An ×, on red while the mouse is over it."""
        if hovered:
            painter.rect_filled(rect, 4, CLOSE_HOVER)
        stroke = egui.Stroke(1.6, WHITE if hovered else TEXT)
        c, r = rect.center(), rect.width() * 0.22
        painter.line_segment(egui.Pos2(c.x - r, c.y - r), egui.Pos2(c.x + r, c.y + r), stroke)
        painter.line_segment(egui.Pos2(c.x - r, c.y + r), egui.Pos2(c.x + r, c.y - r), stroke)

    def _draw_mark_bar(
        self, ui: egui.Ui, painter: egui.Painter, area: egui.Rect, count: int, hidden: int, screens: bool, right: float
    ):
        """The header while windows are marked: how many, and buttons acting on them.
        Returns what a clicked button does, to run after the frame."""
        center_y = area.min.y + HEADER_HEIGHT / 2
        font = egui.FontId.proportional(MARK_BAR_FONT)
        summary = f"{count} marked" + (f" ({hidden} hidden)" if hidden else "")
        x = painter.text(
            egui.Pos2(area.min.x + PADDING, center_y), egui.Align2.LEFT_CENTER, summary, egui.FontId.proportional(15.0), MARKED
        ).max.x + 12
        buttons = [
            ("Close", lambda pos: self.close_marked),
            ("Minimize", lambda pos: self.minimize_marked),
            ("Restore", lambda pos: self.restore_marked),
            ("Snap  >", lambda pos: lambda: self.open_bar_dropdown("snap"))
            if count == 1
            else ("Layout  >", lambda pos: lambda: self.open_bar_dropdown("layout")),
            ("Move to desktop  >", lambda pos: lambda: self.open_bar_dropdown("desktop")),
        ]
        if screens:
            buttons.append(("Move to screen  >", lambda pos: lambda: self.open_bar_dropdown("screen")))
        buttons.append(("Clear", lambda pos: self.clear_marks))
        pages = {"Snap  >": "snap", "Layout  >": "layout", "Move to desktop  >": "desktop", "Move to screen  >": "screen"}
        menu = self.menu
        open_page = menu.page if menu is not None and menu.dropdown else None
        anchors = {}
        clicked = None
        for label, make in buttons:
            galley = painter.layout_no_wrap(label, font, TEXT)
            size = galley.size()
            pill = egui.Rect.from_min_size(
                egui.Pos2(x, center_y - size.y / 2 - 3), egui.Vec2(size.x + 16, size.y + 6)
            )
            if pill.max.x > right:
                break
            response = hit(ui, pill, "marked:" + label)
            describe(response, egui.WidgetType.Button, label)
            page = pages.get(label)
            if page:
                # Where its dropdown opens, for voice and the arrow keys too.
                anchors[page] = egui.Pos2(pill.min.x, pill.max.y + 2)
            painter.rect_filled(pill, 5, CHIP if page and page == open_page else TILE_HOVER if response.hovered() else TILE)
            painter.rect_stroke(pill, 5, egui.Stroke(1.0, BORDER), egui.StrokeKind.Inside)
            painter.galley(egui.Pos2(pill.min.x + 8, pill.min.y + 3), galley, TEXT)
            if response.clicked():
                clicked = make(egui.Pos2(pill.min.x, pill.max.y + 2))
            x = pill.max.x + 6
        self.bar_anchors = anchors
        return clicked

    def _draw_badges(self, painter: egui.Painter, badges: list, right: float, center_y: float) -> float:
        """Small pills drawn right to left ending at `right`; returns where they start."""
        font = egui.FontId.proportional(12.0)
        for text, color in badges:
            galley = painter.layout_no_wrap(text, font, WHITE)
            size = galley.size()
            pill = egui.Rect.from_min_size(
                egui.Pos2(right - size.x - 12, center_y - size.y / 2 - 2), egui.Vec2(size.x + 12, size.y + 4)
            )
            painter.rect_filled(pill, pill.height() / 2, color)
            painter.galley(egui.Pos2(pill.min.x + 6, pill.min.y + 2), galley, WHITE)
            right = pill.min.x - 6
        return right

    def _draw_minimap(self, painter: egui.Painter, rect: egui.Rect, placement: Placement):
        """The screen in miniature with the layout's slots; the current one filled."""
        r = placement.screen.visible_rect
        aspect = r.width / max(r.height, 1)
        h = min(rect.height(), rect.width() / aspect)
        w = h * aspect
        screen = egui.Rect.from_center_size(rect.center(), egui.Vec2(w, h))
        painter.rect_filled(screen, 2, TILE)
        placed_slots = set(placement.placed.values())
        for i, slot in enumerate(placement.slots):
            try:
                left, top, right, bottom = slot_fractions(slot)
            except Exception:
                continue
            cell = egui.Rect.from_min_max(
                egui.Pos2(screen.min.x + w * left, screen.min.y + h * top),
                egui.Pos2(screen.min.x + w * right, screen.min.y + h * bottom),
            ).shrink(1.0)
            if i == placement.index:
                painter.rect_filled(cell, 1, SELECTED)
            elif slot in placed_slots:
                painter.rect_filled(cell, 1, CHIP)
            painter.rect_stroke(cell, 1, egui.Stroke(1.0, TEXT), egui.StrokeKind.Inside)

    def _pointer_moved(self, pos: "egui.Pos2 | None") -> bool:
        """Whether the mouse moved since the switcher opened.

        The window can open under a resting cursor, which egui reports as movement;
        that must not move the selection away from the window the user wants.
        """
        if pos is None:
            return False
        point = (round(pos.x), round(pos.y))
        if self.pointer_origin is None:
            self.pointer_origin = point
        return point != self.pointer_origin

    def _handle_input(self, inp: egui.InputState, cols: int, grid: bool):
        """This frame's typing and keys, as one action to run after render.

        Text goes into the search field. Up/Down move the selection by a row,
        Left/Right only while the field is empty (in the grid), Tab locks "app:<name>"
        in as a chip, Backspace in an empty field removes the chip, Enter focuses the
        selected window, and Escape clears the marks, then the search, then closes the
        switcher. Ctrl+Space marks the selected tile, Shift+arrows mark as they move,
        Ctrl+A marks every tile (with an empty field), Delete closes the marked windows
        or the selected one, and Shift+F10 opens the marked windows' menu.
        """
        ops = []
        events = inp.events()
        # Ctrl+Space marks and Alt+letter jumps; don't also type their characters.
        ctrl_space = any(
            e.kind() == "Key" and e.pressed() and KEY_NAMES.get(repr(e.key())) == "Space" and e.modifiers() is not None and e.modifiers().ctrl
            for e in events
        )
        alt_letter = self.mode == "launcher" and any(
            e.kind() == "Key" and e.pressed() and len(KEY_NAMES.get(repr(e.key())) or "") == 1 and e.modifiers() is not None and e.modifiers().alt
            for e in events
        )
        for event in events:
            kind = event.kind()
            if kind in ("Text", "Paste"):
                text = "".join(ch for ch in event.text() or "" if ch.isprintable())
                if (ctrl_space and not text.strip()) or alt_letter:
                    continue
                if text and self.menu is not None:
                    # Digits pick the numbered menu items; other typing waits.
                    for digit in (ch for ch in text if ch in "123456789"):
                        ops.append(lambda digit=digit: self.pick_menu_item(int(digit)))
                elif text:
                    ops.append(lambda text=text: self.set_query(self.query + text))
                continue
            if kind != "Key" or not event.pressed():
                continue
            key = KEY_NAMES.get(repr(event.key()))
            modifiers = event.modifiers()
            ctrl = bool(modifiers is not None and modifiers.ctrl)
            shift = bool(modifiers is not None and modifiers.shift)
            alt = bool(modifiers is not None and modifiers.alt)
            if self.menu is not None:
                # An open menu takes every key; nothing reaches the tiles or the search.
                if key in ("ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Home", "End", "Enter"):
                    ops.append(lambda key=key: self.menu_key(key))
                elif key == "Escape":
                    ops.append(self.escape)
                continue
            if key == "F10" and shift:
                ops.append(lambda: self.open_marked_menu() if self.marked else self.open_menu(self.selected + 1))
            elif key == "Space" and ctrl:
                ops.append(lambda: self.mark([self.selected + 1]))
            elif key == "D" and ctrl and self.mode == "launcher":
                ops.append(lambda: self.set_launcher_details(None))
            elif key == "D" and ctrl and self.mode == "apps":
                ops.append(lambda: self.set_apps_details(not self.apps_details))
            elif key == "D" and ctrl and self.mode == "windows":
                ops.append(lambda: self.show_window_details(not self.window_details))
            elif key == "A" and ctrl:
                ops.append(lambda: self.query or self.mark_all())
            elif key and len(key) == 1 and alt and self.mode == "launcher":
                # Alt+letter jumps in the launcher (plain letters go to the search).
                ops.append(lambda key=key: self.jump(key))
            elif key in ("PageUp", "PageDown"):
                ops.append(lambda key=key: self.move_row((-1 if key == "PageUp" else 1) * self.page_rows))
            elif key in ("Home", "End"):
                ops.append(lambda key=key: self.move_to_end(key == "End"))
            elif key == "ArrowUp":
                ops.append(lambda shift=shift: self.move_row(-1, mark=shift))
            elif key == "ArrowDown" and self.mode == "apps" and not shift and not self.apps_details:
                ops.append(lambda: self.show_app_windows(self.selected + 1))
            elif key == "ArrowDown":
                ops.append(lambda shift=shift: self.move_row(1, mark=shift))
            elif key in ("ArrowLeft", "ArrowRight") and grid:
                step = -1 if key == "ArrowLeft" else 1
                ops.append(lambda step=step, shift=shift: (self.query and not shift) or self.move_selection(step, mark=shift))
            elif key == "Backspace":
                ops.append(lambda ctrl=ctrl: self.backspace(word=ctrl))
            elif key == "Tab" and ctrl and self.mode in ("windows", "apps"):
                ops.append(self.switch_view)
            elif key == "Tab":
                ops.append(self.lock_tag)
            elif key == "Enter":
                ops.append(lambda: self.select(self.selected + 1))
            elif key == "Escape":
                ops.append(self.escape)
            elif key == "Delete":
                ops.append(lambda: self.close_marked(fallback=True))
        if not ops:
            return None
        return lambda: [op() for op in ops]

    def _draw_search(
        self, ui: egui.Ui, painter: egui.Painter, field: egui.Rect, chip: Chip | None, query: str
    ):
        """The search field: the app chip as a pill, then the text and a caret."""
        # Painted, not an egui TextEdit (the switcher takes the typing itself), so it
        # gets its accessibility node here: an edit named "Search" with the text.
        try:
            info = egui.WidgetInfo.text_edit(True, query, query, "Search")
            info.label = "Search"
            hit(ui, field, "search").widget_info(info)
        except Exception as e:
            print(f"thumbnail_switcher: naming the search field failed: {e!r}")
        painter.rect_filled(field, 6, TILE)
        painter.rect_stroke(field, 6, egui.Stroke(1.5, SELECTED), egui.StrokeKind.Inside)
        center_y = field.center().y
        font = egui.FontId.proportional(15.0)
        x = field.min.x + 8

        if chip is not None:
            galley = painter.layout_no_wrap(f"{chip.tag} {chip.label}  ×", font, WHITE)
            size = galley.size()
            pill = egui.Rect.from_min_size(
                egui.Pos2(x, center_y - size.y / 2 - 3), egui.Vec2(size.x + 16, size.y + 6)
            )
            response = hit(ui, pill, "chip")
            describe(response, egui.WidgetType.Button, f"Remove filter {chip.tag}{chip.label}")
            painter.rect_filled(pill, pill.height() / 2, TILE_HOVER if response.hovered() else CHIP)
            painter.galley(egui.Pos2(pill.min.x + 8, pill.min.y + 3), galley, WHITE)
            if response.clicked():
                cron.after("0ms", lambda: self.set_chip(None))
            x = pill.max.x + 8

        if query:
            text_rect = painter.text(egui.Pos2(x, center_y), egui.Align2.LEFT_CENTER, query, font, TEXT)
            caret_x = text_rect.max.x + 2
        else:
            hint = f'Search titles and apps; "{APP_TAG}name", "{DESK_TAG}2" or "{SCREEN_TAG}2" + Tab filters'
            if chip is not None:
                hint = "Search these windows; Backspace shows all"
            painter.text(egui.Pos2(x + 4, center_y), egui.Align2.LEFT_CENTER, hint, font, DIM_TEXT)
            caret_x = x + 1
        painter.vline(caret_x, center_y - 9, center_y + 9, egui.Stroke(1.5, TEXT))

    def _draw_icon(self, ui: egui.Ui, painter: egui.Painter, entry: Entry, thumb: egui.Rect):
        """The app's icon, large and centered, with "<app> (minimized)" underneath."""
        label_h = 20.0
        size = min(ICON_POINTS, thumb.width(), thumb.height() - label_h - 8)
        center = thumb.center()
        top = center.y - (size + 8 + label_h) / 2
        texture = self._texture(ui, entry)
        if texture is not None and size > 0:
            rect = egui.Rect.from_min_size(
                egui.Pos2(center.x - size / 2, top), egui.Vec2(size, size)
            )
            uv = egui.Rect.from_min_max(egui.Pos2(0.0, 0.0), egui.Pos2(1.0, 1.0))
            painter.image(texture.id(), rect, uv, WHITE)
            text_y = top + size + 8 + label_h / 2
        else:
            text_y = center.y
        painter.text(
            egui.Pos2(center.x, text_y),
            egui.Align2.CENTER_CENTER,
            elide(entry.state_label(), thumb.width(), 14.0),
            egui.FontId.proportional(14.0),
            DIM_TEXT,
        )

    def _texture(self, ui: egui.Ui, entry: Entry) -> "egui.TextureHandle | None":
        """The entry's icon as an egui texture, created on first use."""
        if entry.icon is None:
            return None
        icon = entry.icon
        key = (entry.hwnd, icon.width)
        with self.lock:
            texture = self.textures.get(key)
        if texture is None:
            image = egui.ColorImage.from_rgba_unmultiplied(icon.width, icon.height, icon.rgba)
            texture = ui.ctx().load_texture(
                f"thumbnail_switcher_icon_{entry.hwnd}_{icon.width}",
                image,
                egui.TextureOptions.linear(),
            )
            with self.lock:
                self.textures[key] = texture
        return texture

    def _menu_icon(self, ui: egui.Ui, icon_of) -> "egui.TextureHandle | None":
        """A jump list entry's icon as a texture; fetched in the background the first
        time (the menu redraws when it arrives), None until then or if it has none."""
        entry, app_id = icon_of
        key = ("jump", entry.kind, entry.path or hash(entry.data))
        with self.lock:
            if key in self.textures:
                return self.textures[key]
            icon = self.jump_icons.get(key, False)
            if icon is False:
                self.jump_icons[key] = None
        if icon is False:

            def fetch():
                try:
                    source = jump_lists.icon_source(entry, app_id)
                    # A logo image (Windows Terminal's profiles): its picture, not a
                    # PNG file's icon.
                    picture = entry.kind == "link" and bool(source) and source.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
                    found = window_icons.shell_pixels(source, 32, thumbnail=picture) if source else None
                except Exception:
                    found = None
                with self.lock:
                    self.jump_icons[key] = found
                self.refresh()

            threading.Thread(target=fetch, name="jump list icon", daemon=True).start()
            return None
        if icon is None:
            return None
        image = egui.ColorImage.from_rgba_unmultiplied(icon.width, icon.height, icon.rgba)
        texture = ui.ctx().load_texture(f"thumbnail_switcher_jump_{abs(hash(key))}", image, egui.TextureOptions.linear())
        with self.lock:
            self.textures[key] = texture
        return texture

    def shutdown(self):
        """Stop for good (hot reload): hide, stop the timer, close the window."""
        self.hide()
        self.overlay.close()
        self.grid_overlay.close()
        cron.cancel(self.tick_job)
        self.window.close()


def dump_uia(max_depth: int = 8):
    """Print the switcher window's UI Automation tree, as hinting tools see it."""
    from collections import Counter

    pid = os.getpid()
    windows = [w for w in ui.windows() if w.title == WINDOW_TITLE and w.app.pid == pid]
    if not windows:
        print("thumbnail_switcher: UIA dump: window not found")
        return
    counts = Counter()
    lines = []

    def walk(el, depth):
        try:
            kind = str(el.control_type)
            name = el.name
        except Exception as e:
            lines.append("  " * depth + f"<error {e!r}>")
            return
        counts[kind] += 1
        if len(lines) < 120:
            lines.append("  " * depth + f"{kind} {name!r}")
        if depth >= max_depth:
            return
        try:
            for child in el.children:
                walk(child, depth + 1)
        except Exception as e:
            lines.append("  " * depth + f"<children error {e!r}>")

    walk(windows[0].element, 0)
    print("thumbnail_switcher: UIA dump\n" + "\n".join(lines))
    print(f"thumbnail_switcher: UIA counts {dict(counts)}")


def tiles() -> "Switcher | None":
    """The switcher, for commands naming tiles by number; None while a right-click menu
    is open, so that its numbered items take the numbers instead."""
    return switcher if switcher and switcher.menu is None else None


def with_windows(windows: list[ui.Window], extra: list[ui.Window]) -> list[ui.Window]:
    """`windows` plus any of `extra` it lacks, in z-order."""
    ids = {w.id for w in windows}
    return sort_by_z_order(windows + [w for w in extra if w.id not in ids])


# Talon hot-reloads modules, but the previous module's Switcher keeps its window, cron
# job and DWM thumbnails alive. Keep the live one somewhere that survives reloads so the
# next load can shut it down.
_STASH = "_talon_thumbnail_switcher_instance"

switcher: Switcher | None = None


def on_ready():
    global switcher
    if app.platform != "windows":
        return
    previous = getattr(sys, _STASH, None)
    if previous is not None:
        try:
            previous.shutdown()
        except Exception as e:
            print(f"thumbnail_switcher: shutting down the previous switcher failed: {e!r}")
    switcher = Switcher()
    setattr(sys, _STASH, switcher)


app.register("ready", on_ready)


@mod.action_class
class Actions:
    def thumbnail_switcher_show_all():
        """Show thumbnails of every open and minimized window"""
        if switcher:
            switcher.show(all_windows())

    def thumbnail_switcher_show_application(name: str):
        """Show thumbnails of every window, filtered to one running application"""
        if switcher:
            label = name.split("-::*::-")[0]
            windows = application_windows(name)
            if windows:
                # E.g. "Microsoft Edge-::*::-<a PWA's id>": named like on the taskbar.
                label = app_identity.resolve(windows[0].id, label).name
            everything = with_windows(all_windows(), windows)
            splits = name.split("-::*::-")
            if windows and len(splits) > 2:
                # "<host app>-::*::-None-::*::-<window title>", community's entries for
                # MMC consoles: just that console, under its taskbar name.
                first = Entry(next((w for w in windows if w.title == splits[2]), windows[0]), True)
                label = first.app_name
                windows = [w for w in windows if app_key(Entry(w, True)) == app_key(first)]
            if not windows:
                # A name that isn't exactly Talon's app name, e.g. "Paint" for mspaint.exe.
                label = resolve_app([app_names(w) for w in everything], label) or label
                windows = [w for w in everything if app_names(w)[0] == label]
            switcher.show(everything, windows or None, label)

    def thumbnail_switcher_show_focused_application():
        """Show thumbnails of every window, filtered to the focused application"""
        if switcher:
            active = ui.active_app()
            windows = sort_by_z_order([w for w in active.windows() if is_candidate(w)])
            switcher.show(with_windows(all_windows(), windows), windows, active.name)

    def thumbnail_switcher_search(text: str):
        """Set the thumbnail switcher's search text"""
        if switcher:
            switcher.set_query(text)

    def thumbnail_switcher_app(name: str):
        """Filter the thumbnail switcher to one running application"""
        if switcher:
            switcher.set_app(name.split("-::*::-")[0])

    def thumbnail_switcher_clear():
        """Clear the thumbnail switcher's search text and app filter"""
        if switcher:
            switcher.set_query("")
            switcher.set_chip(None)

    def thumbnail_switcher_close(numbers: list[int]):
        """Close the windows with these numbers in the thumbnail switcher"""
        if tiles():
            switcher.close_windows(numbers)

    def thumbnail_switcher_minimize(numbers: list[int]):
        """Minimize the windows with these numbers in the thumbnail switcher"""
        if tiles():
            switcher.minimize_windows(numbers)

    def thumbnail_switcher_restore(numbers: list[int]):
        """Restore the minimized windows with these numbers in the thumbnail switcher"""
        if tiles():
            switcher.restore_windows(numbers)

    def thumbnail_switcher_maximize(number: int):
        """Maximize and focus the window with this number in the thumbnail switcher"""
        if tiles():
            switcher.maximize_window(number)

    def thumbnail_switcher_snap(number: int, position: Any):
        """Snap the window with this number to a position (user.window_snap_position) and focus it"""
        if tiles():
            switcher.snap_window(number, position)

    def thumbnail_switcher_layout(numbers: list[int], layout: str):
        """Lay out the windows with these numbers side by side (user.thumbnail_switcher_layouts)"""
        if tiles():
            switcher.layout_windows(numbers, LAYOUTS[layout])

    def thumbnail_switcher_move_to_screen(number: int, screen: int):
        """Move the window with this number to a screen and focus it"""
        if tiles():
            switcher.move_to_screen(number, screen=screen)

    def thumbnail_switcher_move_next_screen(number: int):
        """Move the window with this number to the next screen and focus it"""
        if tiles():
            switcher.move_to_screen(number, offset=1)

    def thumbnail_switcher_move_previous_screen(number: int):
        """Move the window with this number to the previous screen and focus it"""
        if tiles():
            switcher.move_to_screen(number, offset=-1)

    def thumbnail_switcher_move_to_desktop(numbers: list[int], desktop: int):
        """Move the windows with these numbers to a virtual desktop"""
        if tiles():
            switcher.move_to_desktop(numbers, number=desktop)

    def thumbnail_switcher_move_next_desktop(numbers: list[int]):
        """Move the windows with these numbers to the next virtual desktop"""
        if tiles():
            switcher.move_to_desktop(numbers, offset=1)

    def thumbnail_switcher_move_previous_desktop(numbers: list[int]):
        """Move the windows with these numbers to the previous virtual desktop"""
        if tiles():
            switcher.move_to_desktop(numbers, offset=-1)

    def thumbnail_switcher_screen(screen: int):
        """Filter the thumbnail switcher to the windows on one screen"""
        if switcher:
            switcher.set_screen(screen)

    def thumbnail_switcher_desk(desktop: int):
        """Filter the thumbnail switcher to the windows on one virtual desktop"""
        if switcher:
            switcher.set_desk(desktop)

    def thumbnail_switcher_place(layout: str):
        """Fill a layout (user.thumbnail_switcher_layouts) slot by slot, picking windows by number"""
        if switcher:
            if not switcher.showing:
                switcher.show(all_windows())
            switcher.start_placement(layout)

    def thumbnail_switcher_skip():
        """While placing windows into a layout, leave the current slot empty"""
        if switcher:
            switcher.skip_slot()

    def thumbnail_switcher_cancel():
        """Close the menu, else leave placement mode, else clear the marks, else close the thumbnail switcher"""
        if switcher:
            if switcher.menu is not None:
                switcher.close_menu()
            elif switcher.placement is not None:
                switcher.end_placement()
            elif switcher.marked:
                switcher.clear_marks()
            else:
                switcher.cancel()

    def thumbnail_switcher_mark(numbers: list[int]):
        """Mark (or unmark, when marked) the windows with these numbers in the thumbnail switcher"""
        if tiles():
            switcher.mark(numbers)

    def thumbnail_switcher_mark_range(first: int, last: int):
        """Mark the windows with numbers first through last in the thumbnail switcher"""
        if tiles():
            switcher.mark_range(first, last)

    def thumbnail_switcher_unmark(numbers: list[int]):
        """Unmark the windows with these numbers in the thumbnail switcher"""
        if tiles():
            switcher.mark(numbers, on=False)

    def thumbnail_switcher_mark_all():
        """Mark every window the thumbnail switcher's search shows"""
        if tiles():
            switcher.mark_all()

    def thumbnail_switcher_clear_marks():
        """Unmark every window in the thumbnail switcher"""
        if tiles():
            switcher.clear_marks()

    def thumbnail_switcher_marked_button(name: str):
        """Do what the marked windows' bar button `name` does: close, minimize, restore,
        clear, or open its menu (snap with one marked, layout with several, move to
        desktop, move to screen). Also while a menu is open: that menu gives way to this one."""
        if not switcher or not switcher.showing or not switcher.marked:
            return
        pages = {"snap": "snap", "layout": "layout", "snap layout": "layout", "move to desktop": "desktop", "move to screen": "screen"}
        if name in pages:
            if name == "move to screen" and switcher.screen_count < 2:
                return
            switcher.open_bar_dropdown(pages[name])
        else:
            {"close": switcher.close_marked, "minimize": switcher.minimize_marked, "restore": switcher.restore_marked, "clear": switcher.clear_marks}[name]()

    def thumbnail_switcher_marked_menu():
        """Open the menu of the marked windows in the thumbnail switcher"""
        if tiles():
            switcher.open_marked_menu()

    def thumbnail_switcher_close_marked():
        """Close the marked windows in the thumbnail switcher"""
        if tiles():
            switcher.close_marked()

    def thumbnail_switcher_minimize_marked():
        """Minimize the marked windows in the thumbnail switcher"""
        if tiles():
            switcher.minimize_marked()

    def thumbnail_switcher_restore_marked():
        """Restore the marked windows in the thumbnail switcher"""
        if tiles():
            switcher.restore_marked()

    def thumbnail_switcher_layout_marked(layout: str):
        """Snap the marked windows into a layout (user.thumbnail_switcher_layouts), in the order they were marked"""
        if tiles():
            switcher.layout_marked(layout)

    def thumbnail_switcher_move_marked_to_screen(screen: int):
        """Move the marked windows to a screen"""
        if tiles():
            switcher.move_marked_to_screen(screen=screen)

    def thumbnail_switcher_move_marked_next_screen():
        """Move the marked windows to the next screen"""
        if tiles():
            switcher.move_marked_to_screen(offset=1)

    def thumbnail_switcher_move_marked_previous_screen():
        """Move the marked windows to the previous screen"""
        if tiles():
            switcher.move_marked_to_screen(offset=-1)

    def thumbnail_switcher_move_marked_to_desktop(desktop: int):
        """Move the marked windows to a virtual desktop"""
        if tiles():
            switcher.move_marked_to_desktop(number=desktop)

    def thumbnail_switcher_move_marked_next_desktop():
        """Move the marked windows to the next virtual desktop"""
        if tiles():
            switcher.move_marked_to_desktop(offset=1)

    def thumbnail_switcher_move_marked_previous_desktop():
        """Move the marked windows to the previous virtual desktop"""
        if tiles():
            switcher.move_marked_to_desktop(offset=-1)

    def thumbnail_switcher_show_apps():
        """Show one icon per running application, like Cmd+Tab"""
        if switcher:
            switcher.show(all_windows(), mode="apps")

    def thumbnail_switcher_show_launcher():
        """Show the app launcher: running apps, then every installed app"""
        if switcher:
            switcher.show(all_windows() or [], mode="launcher")

    def thumbnail_switcher_switch_view(mode: str):
        """In the thumbnail switcher: show the running apps ("apps") or the windows
        ("windows"), without the search or filters"""
        if switcher and switcher.showing:
            switcher.switch_view(mode)

    def thumbnail_switcher_show_apps_details(details: int):
        """Show the running applications as a details table (1) or as icons (0)"""
        if switcher:
            switcher.apps_details = bool(details)
            switcher.show(all_windows(), mode="apps")

    def thumbnail_switcher_show_window_details():
        """Show every open window as a details table, a row per window ("focus window")"""
        if switcher:
            switcher.show(all_windows() or [], mode="windows", window_details=True)

    def thumbnail_switcher_show_all_details(details: int):
        """Show the window list as a details table (1) or as thumbnails/list (0)"""
        if switcher:
            switcher.show(all_windows() or [], mode="windows", window_details=bool(details))

    def thumbnail_switcher_launcher_layout(details: int):
        """Show the app launcher as a details table (1) or an icon grid (0), opening it if needed"""
        details = bool(details)
        if switcher:
            if not (switcher.showing and switcher.mode == "launcher"):
                switcher.launcher_details = details
                switcher.show(all_windows() or [], mode="launcher")
            else:
                switcher.set_launcher_details(details)

    def thumbnail_switcher_sort(column: str):
        """In the app launcher's details view: sort by a column (user.thumbnail_switcher_columns); again to reverse"""
        if switcher:
            switcher.sort_launcher(column)

    def thumbnail_switcher_menu_button(kind: str, number: int):
        """In a jump list menu: pin, unpin or remove the entry with this number ("pin", "unpin" or "remove")"""
        if switcher:
            switcher.menu_button(kind, number)

    def thumbnail_switcher_jump(letter: str):
        """In the app launcher: jump to the installed apps starting with this letter ("#" for digits and symbols)"""
        if tiles():
            switcher.jump(letter)

    def thumbnail_switcher_launch_new(number: int):
        """In the app launcher or apps strip: launch the app with this number (another instance if it's running)"""
        if tiles():
            switcher.launch(number)

    def thumbnail_switcher_app_windows(number: int):
        """In the apps view: show the windows of the app with this number"""
        if tiles():
            switcher.show_app_windows(number)

    def thumbnail_switcher_menu_back():
        """Back from a submenu of the thumbnail switcher's right-click menu"""
        if switcher:
            switcher.menu_back()

    def thumbnail_switcher_dump_uia():
        """Print the thumbnail switcher's UI Automation tree to the Talon log (debugging)"""
        dump_uia()

    def thumbnail_switcher_close_menu():
        """Close the thumbnail switcher's right-click menu, keeping the switcher open"""
        if switcher:
            switcher.close_menu()

    def thumbnail_switcher_menu(number: int):
        """Open the right-click menu of the window with this number in the thumbnail switcher"""
        if switcher:
            switcher.open_menu(number)

    def thumbnail_switcher_select(index: int):
        """Focus the window with the given number in the thumbnail switcher"""
        if switcher:
            switcher.select(index)

    def thumbnail_switcher_hide():
        """Close the thumbnail switcher"""
        if switcher:
            switcher.cancel()
