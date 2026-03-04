import os
import pathlib

from talon import Module, actions

DISTANCE_TO_COMMUNITY_ROOT_DIRECTORY: int = 3
stored_state_directory = None

mod = Module()


@mod.action_class
class Actions:
    def stored_state_does_file_exist(name: str) -> bool:
        """Returns if file exists with that name in the stored state directory"""
        path = compute_stored_state_path(name)
        return path.exists()

    def stored_state_create_signal_file(name: str):
        """Creates an empty file with that name in the stored state directory"""
        path = compute_stored_state_path(name)
        with open(path, "w") as f:
            pass

    def stored_state_set_value(name: str, value: str):
        """Stores the value in the file with that name in the stored state directory"""
        path = compute_stored_state_path(name)
        with open(path, "w") as f:
            f.write(value)

    def storage_state_get_text(name: str) -> str:
        """Gets the text from the file with specified name in the stored state directory"""
        path = compute_stored_state_path(name)
        with open(path, "r") as f:
            return f.read()

def compute_stored_state_path(file_name: str):
    """Returns the path to the specified file in the stored state directory"""
    if stored_state_directory is None:
        raise ValueError(
            "Tried to access the stored state directory before it was defined. Use the on_ready pattern if you need to use stored state on startup."
        )
    return stored_state_directory / file_name


def setup_directory():
    global stored_state_directory
    path_to_file = pathlib.Path(__file__)
    path = path_to_file
    for _ in range(DISTANCE_TO_COMMUNITY_ROOT_DIRECTORY):
        path = path.parent
    stored_state_directory = path / "stored_state"
    if not stored_state_directory.exists():
        os.makedirs(stored_state_directory, exist_ok=True)

setup_directory()