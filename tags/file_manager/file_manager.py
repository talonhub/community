import math
from itertools import islice
from pathlib import Path

from talon import Context, Module, actions, app, imgui, registry, settings, ui

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

setting_auto_show_pickers = mod.setting(
    "file_manager_auto_show_pickers",
    type=int,
    default=0,
    desc="Enable to show the file/directories pickers automatically",
)
setting_folder_limit = mod.setting(
    "file_manager_folder_limit",
    type=int,
    default=1000,
    desc="Maximum number of files/folders to iterate",
)
setting_file_limit = mod.setting(
    "file_manager_file_limit",
    type=int,
    default=1000,
    desc="Maximum number of files to iterate",
)
setting_imgui_limit = mod.setting(
    "file_manager_imgui_limit",
    type=int,
    default=20,
    desc="Maximum number of files/folders to display in the imgui",
)
setting_imgui_string_limit = mod.setting(
    "file_manager_string_limit",
    type=int,
    default=20,
    desc="Maximum like of string to display in the imgui",
)
cached_path = None
file_selections = folder_selections = []
current_file_page = current_folder_page = 1

ctx.lists["self.file_manager_directories"] = []
ctx.lists["self.file_manager_files"] = []


@mod.action_class
class Actions:
    def file_manager_current_path() -> str:
        """Returns the current path for the active file manager."""
        return ""

    def file_manager_open_parent():
        """file_manager_open_parent"""
        return

    def file_manager_go_forward():
        """file_manager_go_forward_directory"""

    def file_manager_go_back():
        """file_manager_go_forward_directory"""

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

    def file_manager_update_lists():
        """Forces an update of the lists (e.g., when file or folder created)"""
        update_lists()

    def file_manager_toggle_pickers():
        """Shows the pickers"""
        if gui_files.showing:
            gui_files.hide()
            gui_folders.hide()
        else:
            gui_files.show()
            gui_folders.show()

    def file_manager_hide_pickers():
        """Hides the pickers"""
        if gui_files.showing:
            gui_files.hide()
            gui_folders.hide()

    def file_manager_get_directory_by_index(index: int) -> str:
        """Returns the requested directory for the imgui display by index"""
        index = (current_folder_page - 1) * setting_imgui_limit.get() + index
        assert index < len(folder_selections)
        return folder_selections[index]

    def file_manager_get_file_by_index(index: int) -> str:
        """Returns the requested directory for the imgui display by index"""
        index = (current_file_page - 1) * setting_imgui_limit.get() + index
        assert index < len(file_selections)
        return file_selections[index]

    def file_manager_next_file_page():
        """next_file_page"""
        global current_file_page
        if gui_files.showing:
            if current_file_page != total_file_pages:
                current_file_page += 1
            else:
                current_file_page = 1
            gui_files.show()

    def file_manager_previous_file_page():
        """previous_file_page"""
        global current_file_page
        if gui_files.showing:
            if current_file_page != 1:
                current_file_page -= 1
            else:
                current_file_page = total_file_pages

            gui_files.show()

    def file_manager_next_folder_page():
        """next_folder_page"""
        global current_folder_page
        if gui_folders.showing:
            if current_folder_page != total_folder_pages:
                current_folder_page += 1
            else:
                current_folder_page = 1

            gui_folders.show()

    def file_manager_previous_folder_page():
        """previous_folder_page"""
        global current_folder_page
        if gui_folders.showing:
            if current_folder_page != 1:
                current_folder_page -= 1
            else:
                current_folder_page = total_folder_pages

            gui_folders.show()


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


@imgui.open(y=10, x=900)
def gui_folders(gui: imgui.GUI):
    global current_folder_page, total_folder_pages
    total_folder_pages = math.ceil(
        len(ctx.lists["self.file_manager_directories"]) / setting_imgui_limit.get()
    )
    gui.text(f"Select a directory ({current_folder_page}/{total_folder_pages})")
    gui.line()

    index = 1
    current_index = (current_folder_page - 1) * setting_imgui_limit.get()

    while index <= setting_imgui_limit.get() and current_index < len(folder_selections):
        name = (
            (
                folder_selections[current_index][: setting_imgui_string_limit.get()]
                + ".."
            )
            if len(folder_selections[current_index]) > setting_imgui_string_limit.get()
            else folder_selections[current_index]
        )
        gui.text(f"{index}: {name} ")
        current_index += 1
        index = index + 1

    # if total_folder_pages > 1:
    # gui.spacer()

    # if gui.button('Next...'):
    #    actions.user.file_manager_next_folder_page()

    # if gui.button("Previous..."):
    #   actions.user.file_manager_previous_folder_page()

    gui.spacer()
    if gui.button("Manager close"):
        actions.user.file_manager_hide_pickers()


@imgui.open(y=10, x=1300)
def gui_files(gui: imgui.GUI):
    global file_selections, current_file_page, total_file_pages
    total_file_pages = math.ceil(len(file_selections) / setting_imgui_limit.get())

    gui.text(f"Select a file ({current_file_page}/{total_file_pages})")
    gui.line()
    index = 1
    current_index = (current_file_page - 1) * setting_imgui_limit.get()

    while index <= setting_imgui_limit.get() and current_index < len(file_selections):
        name = (
            (file_selections[current_index][: setting_imgui_string_limit.get()] + "..")
            if len(file_selections[current_index]) > setting_imgui_string_limit.get()
            else file_selections[current_index]
        )

        gui.text(f"{index}: {name} ")
        current_index = current_index + 1
        index = index + 1

    # if total_file_pages > 1:
    #    gui.spacer()

    #    if gui.button('Next...'):
    #        actions.user.file_manager_next_file_page()

    #   if gui.button("Previous..."):
    #        actions.user.file_manager_previous_file_page()


def clear_lists():
    global folder_selections, file_selections
    if (
        len(ctx.lists["self.file_manager_directories"]) > 0
        or len(ctx.lists["self.file_manager_files"]) > 0
    ):
        current_folder_page = current_file_page = 1
        ctx.lists["self.file_manager_directories"] = []
        ctx.lists["self.file_manager_files"] = []
        folder_selections = []
        file_selections = []


def update_gui():
    if gui_folders.showing or setting_auto_show_pickers.get() >= 1:
        gui_folders.show()
        gui_files.show()


def update_lists(path=None):
    global folder_selections, file_selections, current_folder_page, current_file_page
    is_valid_path = False
    if not path:
        path = actions.user.file_manager_current_path()
    directories = {}
    files = {}
    folder_selections = []
    file_selections = []
    # print(path)
    try:
        current_path = Path(path)
        is_valid_path = current_path.is_dir()
    except:
        is_valid_path = False

    if is_valid_path:
        # print("valid..." + str(current_path))
        try:
            directories = get_directory_map(current_path)
            files = get_file_map(current_path)
        except:
            # print("invalid path...")

            directories = {}
            files = {}

    current_folder_page = current_file_page = 1
    ctx.lists["self.file_manager_directories"] = directories
    ctx.lists["self.file_manager_files"] = files

    folder_selections = list(set(directories.values()))
    folder_selections.sort(key=str.casefold)
    file_selections = list(set(files.values()))
    file_selections.sort(key=str.casefold)

    update_gui()


def win_event_handler(window):
    global cached_path

    # on windows, we get events from the clock
    # and such, so this check is important
    if not window.app.exe or window != ui.active_window():
        return

    path = actions.user.file_manager_current_path()

    if "user.file_manager" not in registry.tags:
        actions.user.file_manager_hide_pickers()
        clear_lists()
    elif path:
        if cached_path != path:
            update_lists(path)
    elif cached_path:
        clear_lists()
        actions.user.file_manager_hide_pickers()

    cached_path = path


def register_events():
    ui.register("win_title", win_event_handler)
    ui.register("win_focus", win_event_handler)


# prevent scary errors in the log by waiting for talon to be fully loaded
# before registering the events
app.register("ready", register_events)
