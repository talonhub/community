# notifies the user if the breaking changes document has updated
# this expects the breaking changes document to be two directory levels above the current one

import os

from talon import Module, actions, app, imgui


@imgui.open(y=0)
def notice_gui(gui: imgui.GUI):
    """Notifies the user that breaking changes has changed"""
    pass


def on_ready():
    parent: str = os.path.dirname(__file__)
    current_size: int = get_current_size(parent)
    previous_size_file_name: str = "previous_breaking_changes_size"
    previous_size_path: str = os.path.join(parent, previous_size_file_name)
    could_read_file: bool = False
    try:
        previous_size: int = get_previous_size(previous_size_path)
        could_read_file = True
    except ValueError as ex:
        app.notify(str(ex))
        print(ex)
    if could_read_file and (current_size != previous_size):
        save_size(previous_size_path, current_size)
        notice_gui.show()


def get_current_size(current_directory_path: str) -> int:
    """Gets the current size of the breaking changes file"""
    great_grandparent: str = os.path.dirname(os.path.dirname(current_directory_path))
    breaking_changes_path: str = os.path.join(great_grandparent, "BREAKING_CHANGES.txt")
    stats: os.stat_result = os.stat(breaking_changes_path)
    return stats.st_size


def get_previous_size(path: str) -> int:
    """Get the last read size of the breaking changes file.
    Raises a FileNotFoundError if the size was never recorded.
    Raises a ValueError if the value cannot be parsed"""
    if not os.path.exists(path):
        raise FileNotFoundError()
    with open(path, "r") as f:
        line_text: str = f.readline().strip()
        try:
            size: int = int(line_text)
        except Exception as _:
            raise ValueError(
                f"Could not parse the first line of the file responsible for tracking the previous size of the breaking changes file as an integer: {line_text}"
            )
        return size


def save_size(path: str, size: int):
    """Updates the recorded previous size of the breaking changes file"""
    with open(path, "w") as f:
        value_text = str(size)
        f.write(value_text)


app.register("ready", on_ready)
