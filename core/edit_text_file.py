import os
import subprocess

from talon import Context, Module, app

# path to knausj root directory
REPO_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.join(REPO_DIR, "settings")

mod = Module()
ctx = Context()

mod.list("talon_settings_csv", desc="Absolute paths to talon user settings csv files.")
_csvs = {
    name: os.path.join(SETTINGS_DIR, file_name)
    for name, file_name in {
        "file extensions": "file_extensions.csv",
        "search engines": "search_engines.csv",
        "system paths": "system_paths.csv",
        "websites": "websites.csv",
        "words to replace": "words_to_replace.csv",
        "additional words": "additional_words.csv",
    }.items()
}
_csvs["homophones"] = os.path.join(REPO_DIR, "core", "homophones", "homophones.csv")
ctx.lists["self.talon_settings_csv"] = _csvs


@mod.action_class
class ModuleActions:
    def edit_text_file(path: str):
        """Tries to open a file in the user's preferred text editor."""


winctx, linuxctx, macctx = Context(), Context(), Context()
winctx.matches = "os: windows"
linuxctx.matches = "os: linux"
macctx.matches = "os: mac"


@winctx.action_class("self")
class WinActions:
    def edit_text_file(path):
        # If there's no applications registered that can open the given type
        # of file, 'edit' will fail, but 'open' always gives the user a
        # choice between applications.
        try:
            os.startfile(path, "edit")
        except OSError:
            os.startfile(path, "open")


@macctx.action_class("self")
class MacActions:
    def edit_text_file(path):
        # -t means try to open in a text editor.
        open_with_subprocess(path, ["/usr/bin/open", "-t", path])


@linuxctx.action_class("self")
class LinuxActions:
    def edit_text_file(path):
        # we use xdg-open for this even though it might not open a text
        # editor. we could use $EDITOR, but that might be something that
        # requires a terminal (eg nano, vi).
        open_with_subprocess(path, ["/usr/bin/xdg-open", path])


# Helper for linux and mac.
def open_with_subprocess(path, args):
    """Tries to open a file using the given subprocess arguments."""
    try:
        return subprocess.run(args, timeout=0.5, check=True)
    except subprocess.TimeoutExpired:
        app.notify(f"Timeout trying to open file for editing: {path}")
        raise
    except subprocess.CalledProcessError:
        app.notify(f"Could not open file for editing: {path}")
        raise
