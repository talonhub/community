# notifies the user if the breaking changes document has updated
# this expects the breaking changes document to be two directory levels above the current one
# if the breaking changes file is moved or renamed, update the compute_breaking_changes_path_from_current_directory function

import pathlib

from talon import Context, Module, actions, app, fs, imgui

# used to activate the tag for when the notice is showing
ctx = Context()


DO_NOT_SHOW_BREAKING_CHANGES_FILE_NAME: str = "do_not_show_breaking_changes_notice"
STORED_STATE_SUBDIRECTORY_NAME: str = "breaking_changes_update_notice"


@imgui.open(y=0)
def notice_gui(gui: imgui.GUI):
    """Notifies the user that breaking changes has changed"""
    gui.text("There was a new breaking change.")
    gui.text("A breaking change changes or removes some preexisting functionality.")
    gui.text("We document breaking changes in the BREAKING_CHANGES.txt file.")
    gui.line()
    if gui.button("read breaking changes"):
        actions.user.breaking_changes_open()
    if gui.button("breaking hide"):
        actions.user.breaking_changes_notice_hide()
    if gui.button("breaking dismiss (do not show this again)"):
        actions.user.breaking_changes_notice_never_show_again()


def on_ready():
    show_breaking_changes_message_if_needed()
    fs.watch(compute_breaking_changes_path(), on_breaking_changes_file_change)


def on_breaking_changes_file_change(path, flags):
    show_breaking_changes_message_if_needed()


def show_breaking_changes_message_if_needed():
    """Perform bookkeeping and show gui if the breaking changes file has changed"""
    if should_not_show_breaking_changes_notice():
        return
    try:
        current_size = get_current_breaking_changes_file_size()
    except FileNotFoundError:
        app.notify(
            "The breaking changes file could not be found. Please report this error on the Talon slack or Community GitHub."
        )
        return
    previous_size_file_name = "previous_breaking_changes_size"
    previous_size = compute_previous_breaking_changes_file_size(previous_size_file_name)
    if previous_size is not None and (current_size != previous_size):
        notice_gui.show()
        ctx.tags = ["user.breaking_changes_notice_showing"]
    save_breaking_changes_file_size(previous_size_file_name, current_size)


def compute_previous_breaking_changes_file_size(previous_size_file_name):
    """Computes the previous size of the breaking changes file. Returns None if the value cannot be obtained."""
    try:
        return get_previous_breaking_changes_file_size(previous_size_file_name)
    except ValueError as ex:
        app.notify(str(ex))
        print(ex)
    except FileNotFoundError:
        pass
    return None


def should_not_show_breaking_changes_notice():
    """Determines if the breaking changes notice should not be shown"""
    return actions.user.stored_state_does_file_exist(
        STORED_STATE_SUBDIRECTORY_NAME, DO_NOT_SHOW_BREAKING_CHANGES_FILE_NAME
    )


def get_current_breaking_changes_file_size():
    """Gets the current size of the breaking changes file"""
    breaking_changes_path = compute_breaking_changes_path_from_current_directory()
    stats = breaking_changes_path.stat()
    return stats.st_size


def get_previous_breaking_changes_file_size(name):
    """Get the last read size of the breaking changes file.
    Raises a FileNotFoundError if the size was never recorded.
    Raises a ValueError if the value cannot be parsed"""
    if not actions.user.stored_state_does_file_exist(
        STORED_STATE_SUBDIRECTORY_NAME, name
    ):
        raise FileNotFoundError()
    line_text = actions.user.stored_state_get_text(
        STORED_STATE_SUBDIRECTORY_NAME, name
    ).strip()
    try:
        size = int(line_text)
    except ValueError:
        raise ValueError(
            f"Could not parse the first line of the file responsible for tracking the previous size of the breaking changes file as an integer: {line_text}"
        )
    return size


def save_breaking_changes_file_size(file_name, size):
    """Updates the recorded previous size of the breaking changes file"""
    value_text = str(size)
    actions.user.stored_state_set_value(
        STORED_STATE_SUBDIRECTORY_NAME, file_name, value_text
    )


def compute_breaking_changes_path():
    path = compute_breaking_changes_path_from_current_directory()
    return path


def compute_breaking_changes_path_from_current_directory():
    """Compute the path to the breaking changes file"""
    current_directory = pathlib.Path(__file__).parent
    grandparent = current_directory.parent.parent
    return grandparent / "BREAKING_CHANGES.txt"


mod = Module()

mod.tag(
    "breaking_changes_notice_showing",
    desc="The notification that breaking changes has updated is showing",
)


@mod.action_class
class Actions:
    def breaking_changes_notice_hide():
        """Hide the breaking changes notice"""
        ctx.tags = []
        notice_gui.hide()

    def breaking_changes_notice_never_show_again():
        """Never show the breaking changes notice again"""
        actions.user.breaking_changes_notice_hide()
        actions.user.stored_state_create_signal_file(
            STORED_STATE_SUBDIRECTORY_NAME, DO_NOT_SHOW_BREAKING_CHANGES_FILE_NAME
        )

    def breaking_changes_open():
        """Opens the breaking changes file"""
        path = compute_breaking_changes_path()
        actions.user.edit_text_file(path)


app.register("ready", on_ready)
