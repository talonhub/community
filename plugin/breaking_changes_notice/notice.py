# notifies the user if the breaking changes document has updated
# this expects the breaking changes document to be two directory levels above the current one
# if the breaking changes file is moved or renamed, update the compute_breaking_changes_path_from_current_directory function

import os

from talon import Module, actions, app, imgui, Context

# used to activate the tag for when the notice is showing
ctx = Context()

@imgui.open(y=0)
def notice_gui(gui: imgui.GUI):
    """Notifies the user that breaking changes has changed"""
    gui.text("There are new breaking changes")
    if gui.button("read breaking changes"):
        actions.user.breaking_changes_open()
    if gui.button("breaking hide"):
        actions.user.breaking_changes_notice_hide()


def on_ready():
    parent: str = os.path.dirname(__file__)
    current_size: int = get_current_size(parent)
    previous_size_file_name: str = "previous_breaking_changes_size"
    previous_size_path: str = os.path.join(parent, previous_size_file_name)
    could_read_file: bool = True
    try:
        previous_size: int = get_previous_size(previous_size_path)
    except ValueError as ex:
        could_read_file = False
        app.notify(str(ex))
        print(ex)
    except FileNotFoundError:
        could_read_file = False
    if could_read_file and (current_size != previous_size):
        notice_gui.show()
        ctx.tags = ["user.breaking_changes_notice_showing"]
    save_size(previous_size_path, current_size)


def get_current_size(current_directory_path: str) -> int:
    """Gets the current size of the breaking changes file"""
    breaking_changes_path: str = compute_breaking_changes_path_from_current_directory(
        current_directory_path
    )
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
        except ValueError:
            raise ValueError(
                f"Could not parse the first line of the file responsible for tracking the previous size of the breaking changes file as an integer: {line_text}"
            )
        return size


def save_size(path: str, size: int):
    """Updates the recorded previous size of the breaking changes file"""
    with open(path, "w") as f:
        value_text = str(size)
        f.write(value_text)


def compute_breaking_changes_path_from_current_directory(current_directory: str):
    grandparent: str = os.path.dirname(os.path.dirname(current_directory))
    return os.path.join(grandparent, "BREAKING_CHANGES.txt")


mod = Module()

mod.tag("breaking_changes_notice_showing", desc="The notification that breaking changes has updated is showing")

@mod.action_class
class Actions:
    def breaking_changes_notice_hide():
        """Hide the breaking changes notice"""
        ctx.tags = []
        notice_gui.hide()

    def breaking_changes_open():
        """Opens the breaking changes file"""
        current_directory: str = os.path.dirname(__file__)
        path: str = compute_breaking_changes_path_from_current_directory(
            current_directory
        )
        actions.user.edit_text_file(path)


app.register("ready", on_ready)
