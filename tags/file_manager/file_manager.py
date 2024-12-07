import math
from itertools import islice
from pathlib import Path

from talon import Context, Module, actions, app, imgui, scope, settings, ui

mod = Module()
ctx = Context()

mod.tag("file_manager", desc="Tag for enabling generic file management commands")
mod.list("file_manager_directories", desc="List of subdirectories for the current path")
mod.list("file_manager_files", desc="List of files at the root of the current path")

words_to_exclude = [
    "and",
    "zero",
    "one",
    "two",
    "three",
    "for",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "microsoft",
    "windows",
    "Windows",
    "dot",
    "exe",
]

mod.setting(
    "file_manager_folder_limit",
    type=int,
    default=1000,
    desc="Maximum number of files/folders to iterate",
)
mod.setting(
    "file_manager_file_limit",
    type=int,
    default=1000,
    desc="Maximum number of files to iterate",
)


@mod.action_class
class Actions:
    def file_manager_current_path() -> str:
        """Returns the current path for the active file manager."""
        return ""

    def file_manager_open_parent():
        """file_manager_open_parent"""
        return

    def file_manager_open_volume(volume: str):
        """file_manager_open_volume"""

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""

    def file_manager_select_directory(path: str):
        """selects the directory"""

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""

    def file_manager_show_properties():
        """Shows the properties for the file"""

    def file_manager_terminal_here():
        """Opens terminal at current location"""

    def file_manager_open_file(path: str):
        """opens the file"""

    def file_manager_select_file(path: str):
        """selects the file"""

    def file_manager_refresh_title():
        """Refreshes the title to match current directory. this is for e.g. windows command prompt that will need to do some magic."""
        return


def is_dir(f):
    try:
        return f.is_dir()
    except:
        return False


def is_file(f):
    try:
        return f.is_file()
    except:
        return False


def get_directory_map(current_path):
    directories = [
        f.name
        for f in islice(
            current_path.iterdir(), settings.get("user.file_manager_folder_limit", 1000)
        )
        if is_dir(f)
    ]
    directories.sort(key=str.casefold)
    return actions.user.create_spoken_forms_from_list(
        directories, words_to_exclude=words_to_exclude
    )


def get_file_map(current_path):
    files = [
        f.name
        for f in islice(
            current_path.iterdir(), settings.get("user.file_manager_file_limit", 1000)
        )
        if is_file(f)
    ]
    files.sort(key=str.casefold)
    return actions.user.create_spoken_forms_from_list(
        files, words_to_exclude=words_to_exclude
    )


@ctx.dynamic_list("user.file_manager_directories")
def file_manager_directories(phrase) -> dict[str, str]:
    is_valid_path = False

    path = actions.user.file_manager_current_path()

    directories = {}
    try:
        current_path = Path(path)
        is_valid_path = current_path.is_dir()
    except:
        is_valid_path = False

    if is_valid_path:
        try:
            directories = get_directory_map(current_path)
        except:
            directories = {}

    return directories


@ctx.dynamic_list("user.file_manager_files")
def file_manager_files(phrase) -> dict[str, str]:
    global files
    is_valid_path = False
    path = actions.user.file_manager_current_path()

    files = {}
    try:
        current_path = Path(path)
        is_valid_path = current_path.is_dir()
    except:
        is_valid_path = False

    if is_valid_path:
        try:
            files = get_file_map(current_path)
        except:
            files = {}

    return files
