"""An egui editor for this machine's launch_applications.json (prototype).

Edits `exclude` and `spoken_forms` live: each change is saved a moment later (every other
key is written back as it was read), and changes made to the file elsewhere load in.
app_switcher.py picks up each save through its resource.watch.

Say "launch applications editor" to open it.
"""

import os
import platform
import sys

from talon import Module, app, cron

from ..egui_kit import a11y, native, reload
from ..egui_kit.host import HostWindow
from .launch_editor.editor import Editor, WINDOW_TITLE  # noqa: F401
from .launch_editor.store import FILTERS  # noqa: F401
from .launch_editor.view import EditorMenu  # noqa: F401

# While prototyping: open the editor on every (re)load so render errors show in the log.
DEV_SHOW_ON_LOAD = False

JSON_PATH = os.path.normcase(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        app.platform,
        platform.node(),
        "launch_applications.json",
    )
)


mod = Module()


# Talon hot-reloads modules, but the previous module's Editor keeps its window; the kit's
# HostWindow.replace shuts it down.
_STASH = "_talon_launch_applications_editor_instance"
editor: Editor | None = None


def dump_uia(max_depth: int = 12):
    """Print the editor window's UI Automation tree, as hinting tools see it."""
    a11y.dump_uia(WINDOW_TITLE, "launch_applications_editor", max_depth)


def close_stray_windows():
    """Close any editor window a previous load left behind (e.g. two reloads in quick
    succession), the same way its title bar's X would."""
    print(f"launch_applications_editor: closed {native.close_own_windows(WINDOW_TITLE)} leftover window(s)")


# Modules whose reloads must settle before the editor is rebuilt (see egui_kit/reload).
RELOAD_PREFIXES = (
    "user.community.core.app_switcher.launch_editor.",
    "user.community.core.app_switcher.launch_applications_editor",
    "user.community.core.app_switcher.windows.",
    "user.community.core.egui_kit.",
)


def build():
    """A new editor from the current Editor class (looked up now: this module may have
    re-run before launch_editor/editor.py did)."""
    global editor
    current = sys.modules[__name__.rsplit(".", 1)[0] + ".launch_editor.editor"].Editor
    editor = HostWindow.replace(
        _STASH, lambda: current(JSON_PATH), before_create=close_stray_windows, tag="launch_applications_editor"
    )
    if DEV_SHOW_ON_LOAD:
        editor.show()
        cron.after("4s", dump_uia)


def on_ready():
    reload.when_fresh(RELOAD_PREFIXES, build, tag="launch_applications_editor")


app.register("ready", on_ready)


@mod.action_class
class Actions:
    def launch_applications_editor_show():
        """Show the launch applications editor"""
        if editor:
            editor.show()

    def launch_applications_editor_show_entry(app_id: str):
        """Show the launch applications editor on one entry, by its unique_identifier"""
        if editor and not editor.show_entry(app_id):
            app.notify("Launch applications editor", f"No entry for {app_id}")

    def launch_applications_editor_dump_uia():
        """Print the editor window's UI Automation tree to the Talon log (debugging)"""
        dump_uia()

    def launch_applications_editor_hide():
        """Hide the launch applications editor"""
        if editor:
            editor.hide()
