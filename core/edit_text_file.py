import os
import subprocess
from pathlib import Path

from talon import Context, Module, app

# path to community/knausj root directory
REPO_DIR = os.path.dirname(os.path.dirname(__file__))

mod = Module()
ctx = Context()
mod.list(
    "edit_file",
    desc="Absolute paths to frequently edited files (Talon list, CSV, etc.)",
)

_edit_files = {
    "additional words": "core/vocabulary/vocabulary.talon-list",
    "alphabet": "core/keys/letter.talon-list",
    "homophones": "core/homophones/homophones.csv",
    "search engines": "core/websites_and_search_engines/search_engine.talon-list",
    "unix utilities": "tags/terminal/unix_utility.talon-list",
    "websites": "core/websites_and_search_engines/website.talon-list",
}

_settings_csvs = {
    "abbreviations": "abbreviations.csv",
    "file extensions": "file_extensions.csv",
    "words to replace": "words_to_replace.csv",
}

ctx.lists["self.edit_file"] = {
    **_edit_files,
    **{name: f"settings/{file_name}" for name, file_name in _settings_csvs.items()},
}


@mod.action_class
class ModuleActions:
    def edit_text_file(file: str):
        """Tries to open a file in the user's preferred text editor."""


winctx, linuxctx, macctx = Context(), Context(), Context()
winctx.matches = "os: windows"
linuxctx.matches = "os: linux"
macctx.matches = "os: mac"


@winctx.action_class("self")
class WinActions:
    def edit_text_file(file: str):
        path = get_full_path(file)
        # If there's no applications registered that can open the given type
        # of file, 'edit' will fail, but 'open' always gives the user a
        # choice between applications.
        try:
            os.startfile(path, "edit")
        except OSError:
            os.startfile(path, "open")


@macctx.action_class("self")
class MacActions:
    def edit_text_file(file: str):
        path = get_full_path(file)
        # -t means try to open in a text editor.
        open_with_subprocess(path, ["/usr/bin/open", "-t", path.expanduser().resolve()])


@linuxctx.action_class("self")
class LinuxActions:
    def edit_text_file(file: str):
        path = get_full_path(file)
        # we use xdg-open for this even though it might not open a text
        # editor. we could use $EDITOR, but that might be something that
        # requires a terminal (eg nano, vi).
        try:
            open_with_subprocess(path, ["xdg-open", path.expanduser().resolve()])
        except FileNotFoundError:
            app.notify(f"xdg-open missing. Could not open file for editing: {path}")
            raise


# Helper for linux and mac.
def open_with_subprocess(path: Path, args):
    """Tries to open a file using the given subprocess arguments."""
    try:
        return subprocess.run(args, timeout=0.5, check=True)
    except subprocess.TimeoutExpired:
        app.notify(f"Timeout trying to open file for editing: {path}")
        raise
    except subprocess.CalledProcessError:
        app.notify(f"Could not open file for editing: {path}")
        raise


def get_full_path(file: str) -> Path:
    path = Path(file)
    if not path.is_absolute():
        path = REPO_DIR / path
    return path.resolve()
