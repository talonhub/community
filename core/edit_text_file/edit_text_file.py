import os
import subprocess
from pathlib import Path

from talon import Context, Module, app

# Path to community root directory
REPO_DIR = Path(__file__).parent.parent.parent

mod = Module()
mod.list(
    "edit_text_file",
    desc="Paths to frequently edited files (Talon list, CSV, etc.)",
)

ctx_win, ctx_linux, ctx_mac = Context(), Context(), Context()
ctx_win.matches = "os: windows"
ctx_linux.matches = "os: linux"
ctx_mac.matches = "os: mac"


@mod.action_class
class Actions:
    def edit_text_file(file: str):
        """Tries to open a file in the user's preferred text editor."""


@ctx_win.action_class("user")
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


@ctx_mac.action_class("user")
class MacActions:
    def edit_text_file(file: str):
        path = get_full_path(file)
        # -t means try to open in a text editor.
        open_with_subprocess(path, ["/usr/bin/open", "-t", path.expanduser().resolve()])


@ctx_linux.action_class("user")
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
def open_with_subprocess(path: Path, args: list[str | Path]):
    """Tries to open a file using the given subprocess arguments."""
    try:
        subprocess.run(args, timeout=0.5, check=True)
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
