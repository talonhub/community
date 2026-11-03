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

import sys
from typing import Any

from talon import Context, Module, app, ui

from ...egui_kit import a11y, reload
from ...egui_kit.host import HostWindow
from ..windows import app_identity
from . import launcher_apps
from .config import (  # noqa: F401
    LAYOUTS,
    WINDOW_TITLE,
)
from .model import (  # noqa: F401
    Entry,
    app_key,
    app_names,
    index_letter,
    resolve_app,
)
from .placement import (  # noqa: F401
    slot_rect,
)
from .sources import (  # noqa: F401
    all_windows,
    application_windows,
    is_candidate,
    sort_by_z_order,
    with_windows,
)
from .switcher import (  # noqa: F401
    Switcher,
)


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


@mod.capture(rule="<number_small> ([and] <number_small>)*")
def thumbnail_switcher_numbers(m) -> list[int]:
    """One or more tile numbers: "three", "one and four", "two five"."""
    return m.number_small_list


def dump_uia(max_depth: int = 8):
    """Print the switcher window's UI Automation tree, as hinting tools see it."""
    a11y.dump_uia(WINDOW_TITLE, "thumbnail_switcher", max_depth)


def tiles() -> "Switcher | None":
    """The switcher, for commands naming tiles by number; None while a right-click menu
    is open, so that its numbered items take the numbers instead."""
    return switcher if switcher and switcher.menu is None else None


# Talon hot-reloads modules, but the previous module's Switcher keeps its window, cron
# job and DWM thumbnails alive. Keep the live one somewhere that survives reloads so the
# next load can shut it down.
_STASH = "_talon_thumbnail_switcher_instance"

switcher: Switcher | None = None


# Modules whose reloads must settle before the switcher is rebuilt (see egui_kit/reload).
RELOAD_PREFIXES = ("user.community.core.app_switcher.", "user.community.core.egui_kit.")


def build():
    """A new switcher from the current Switcher class (looked up now: this module may
    have re-run before switcher.py did)."""
    global switcher
    current = sys.modules[__name__.rsplit(".", 1)[0] + ".switcher"].Switcher
    switcher = HostWindow.replace(_STASH, lambda: current(ctx), tag="thumbnail_switcher")


def on_ready():
    if app.platform != "windows":
        return
    reload.when_fresh(RELOAD_PREFIXES, build, tag="thumbnail_switcher")


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
