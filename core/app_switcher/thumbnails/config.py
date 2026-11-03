"""The thumbnail switcher's constants: sizes, colours (from the shared theme), layouts,
columns, keys and timings."""

import egui
from ...egui_kit import widgets
from ...egui_kit import menu as kit_menu
from ...egui_kit.theme import THEME


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
# How long to wait before checking which windows actually closed: some ask to save.
CLOSE_CHECKS = ("300ms", "1500ms")
# Talon window events that can change what the switcher shows.
WINDOW_EVENTS = ("win_open", "win_close", "win_show", "win_hide", "win_title", "win_move", "win_resize")
# Polling fallback for changes Talon has no event for (minimizing), in ticks.
SYNC_EVERY_TICKS = 10
# Commands like maximize briefly activate the window they act on; for this long
# afterwards the switcher takes focus back instead of closing.
HOLD_FOCUS_SECONDS = 1.0
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
BACKGROUND = THEME.bg
TILE = THEME.surface
BORDER = THEME.border
SELECTED = THEME.accent
WHITE = THEME.white
ICON_POINTS = 96.0
TEXT = THEME.text
DIM_TEXT = THEME.text_muted
CHIP = THEME.chip_bg
CURRENT_DESKTOP = THEME.badge_desktop
APP_TAG = "app:"
DESK_TAG = "desk:"
SCREEN_TAG = "screen:"
SCREEN_BADGE = THEME.badge_screen
# Marked tiles (multi-select): the marked bar's summary colour.
MARKED = THEME.mark
MARK_BAR_FONT = 13.0
CLOSE_BUTTON = 22.0  # the header's close button, egui points
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
RUNNING_DOT = THEME.success
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
MENU_BUTTON_TIPS = {"pin": "Pin to this list", "unpin": "Unpin from this list", "remove": "Remove from this list"}
# The menu's rows, gutter and icon column are the kit's (Windows 11 Start menu style).
MENU_WIDTH = kit_menu.WIDTH  # egui points
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
# Controls and accessibility from the kit: stable ids under the "ts:" prefix (UIA ids
# unchanged) and the shared theme.
KIT = widgets.Kit("ts", THEME)
