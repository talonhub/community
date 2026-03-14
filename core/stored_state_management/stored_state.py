# This provides the intended way to manage Community stored state as documented in CONTRIBUTING.md P08.

import pathlib

from talon import Module

# this file is this many directories under community's root directory
DISTANCE_TO_COMMUNITY_ROOT_DIRECTORY: int = 3


def setup_directory():
    """Create the stored state directory if it does not already exist and returns the directory path"""
    path_to_file = pathlib.Path(__file__)
    path = path_to_file
    for _ in range(DISTANCE_TO_COMMUNITY_ROOT_DIRECTORY):
        path = path.parent
    stored_state_directory = path / "stored_state"
    stored_state_directory.mkdir(exist_ok=True)
    return stored_state_directory


stored_state_directory = setup_directory()


mod = Module()


@mod.action_class
class Actions:
    def stored_state_does_file_exist(directory_name: str, name: str):
        """Returns if file exists with that name in the stored state directory"""
        path = stored_state_directory / directory_name / name
        return path.exists()

    def stored_state_create_signal_file(directory_name: str, name: str):
        """Creates an empty file with that name in the stored state directory"""
        path = stored_state_directory / directory_name / name
        create_parent_directory(path)
        with open(path, "w") as f:
            pass

    def stored_state_remove_signal_file(directory_name: str, name: str):
        """Deletes the specified signal file in the stared state directory"""
        path = stored_state_directory / directory_name / name
        if not path.exists():
            return
        elif path.is_dir():
            raise IsADirectoryError(
                f"Tried to remove signal file at path {path} but it was a directory!"
            )
        elif not path.is_file():
            raise OSError(
                f"Tried to remove a signal file at path {path} but it was not a file!"
            )
        elif path.stat().st_size != 0:
            raise ValueError(
                f"Tried to remove signal file at path {path} but it was not empty, so it was not a signal file!"
            )
        path.unlink(missing_ok=True)

    def stored_state_set_value(directory_name: str, name: str, value: str):
        """Stores the value in the file with that name in the stored state directory"""
        path = stored_state_directory / directory_name / name
        create_parent_directory(path)
        with open(path, "w") as f:
            f.write(value)

    def stored_state_get_text(directory_name: str, name: str) -> str:
        """Gets the text from the file with specified name in the stored state directory"""
        path = stored_state_directory / directory_name / name
        with open(path, "r") as f:
            return f.read()


def create_parent_directory(path):
    """Creates the parent directory if it does not exist"""
    parent_dir = path.parent
    parent_dir.mkdir(exist_ok=True)
