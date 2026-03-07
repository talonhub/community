# This provides the intended way to manage Community stored state as documented in CONTRIBUTING.md P08.

import pathlib

from talon import Module

# this file is this many directories under community's root directory
DISTANCE_TO_COMMUNITY_ROOT_DIRECTORY: int = 3
stored_state_directory = None

mod = Module()


@mod.action_class
class Actions:
    def stored_state_does_file_exist(directory_name: str, name: str):
        """Returns if file exists with that name in the stored state directory"""
        path = compute_stored_state_path(directory_name, name)
        return path.exists()

    def stored_state_create_signal_file(directory_name: str, name: str):
        """Creates an empty file with that name in the stored state directory"""
        path = compute_stored_state_path(directory_name, name)
        create_parent_directory(path)
        with open(path, "w") as f:
            pass

    def stored_state_set_value(directory_name: str, name: str, value: str):
        """Stores the value in the file with that name in the stored state directory"""
        path = compute_stored_state_path(directory_name, name)
        create_parent_directory(path)
        with open(path, "w") as f:
            f.write(value)

    def stored_state_get_text(directory_name: str, name: str) -> str:
        """Gets the text from the file with specified name in the stored state directory"""
        path = compute_stored_state_path(directory_name, name)
        with open(path, "r") as f:
            return f.read()


def compute_stored_state_path(directory_name, file_name):
    """Returns the path to the specified file in the stored state directory"""
    if stored_state_directory is None:
        raise ValueError(
            "Tried to access the stored state directory before it was defined. Use the on_ready pattern if you need to use stored state on startup."
        )
    return stored_state_directory / directory_name / file_name


def create_parent_directory(path):
    """Creates the parent directory if it does not exist"""
    parent_dir = path.parent
    parent_dir.mkdir(exist_ok=True)


def setup_directory():
    """Create the stored state directory if it does not already exist"""
    global stored_state_directory
    path_to_file = pathlib.Path(__file__)
    path = path_to_file
    for _ in range(DISTANCE_TO_COMMUNITY_ROOT_DIRECTORY):
        path = path.parent
    stored_state_directory = path / "stored_state"
    stored_state_directory.mkdir(exist_ok=True)


setup_directory()
