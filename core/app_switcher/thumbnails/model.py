"""The switcher's model: a tile per window (Entry) or per app (AppGroup), the app filter
chip, matching, grouping, screens, and the launcher's sections and index letters."""

import os
from talon import ui
from ...egui_kit import table as kit_table
from . import dwm_thumbnails as dwm
from ..windows import virtual_desktops as vd
from ..windows import app_identity
from ..windows import window_filter
from . import launcher_apps
from . import window_icons
from .config import APP_TAG, DETAIL_COLUMNS, LIST_ICON_PIXELS, SORTABLE


window_model_id = app_identity.window_model_id


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


def launch_id(entry) -> str:
    """The app's launch list id (Apps folder id), if it has one."""
    installed = entry if isinstance(entry, launcher_apps.InstalledApp) else getattr(entry, "launch", None)
    return installed.app_id if installed is not None else ""


def detail_columns(width: float, screens: bool, definition=DETAIL_COLUMNS) -> list[kit_table.Placed]:
    """The details view's columns placed across `width` (x from the row's start); the
    name or title column takes the rest, at least 120 points."""
    columns = [kit_table.Column(key, heading, w, sortable=key in SORTABLE) for key, heading, w in definition if key != "screen" or screens]
    return kit_table.column_layout(columns, width, min_flex=120.0)


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
