from talon import app, Module, Context, actions, ui, imgui, settings, app, registry
from os.path import expanduser
from subprocess import Popen
from pathlib import Path
from typing import List, Union
import os
import math
import re
from itertools import islice

mod = Module()
ctx = Context()

mod.tag("file_manager", desc="Tag for enabling generic file management commands")
mod.list("file_manager_directories", desc="List of subdirectories for the current path")
mod.list("file_manager_files", desc="List of files at the root of the current path")


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
        # tbd
        # else is_linux:

    def file_manager_show_properties():
        """Shows the properties for the file"""

    def file_manager_terminal_here():
        """Opens terminal at current location"""

    def file_manager_open_file(path: str):
        """opens the file"""

    def file_manager_select_file(path: str):
        """selects the file"""

    def file_manager_refresh_title():
        """Refreshes the title to match current directory"""
        # todo: this is for e.g. windows command prompt that will need to do some magic.
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
            gui_files.freeze()
            gui_folders.freeze()

    def file_manager_open_user_directory(path: str):
        """expands and opens the user directory"""
        path = os.path.expanduser(os.path.join("~", path))
        actions.user.file_manager_open_directory(path)

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
            gui_files.freeze()

    def file_manager_previous_file_page():
        """previous_file_page"""
        global current_file_page
        if gui_files.showing:
            if current_file_page != 1:
                current_file_page -= 1
            else:
                current_file_page = total_file_pages

            gui_files.freeze()

    def file_manager_next_folder_page():
        """next_folder_page"""
        global current_folder_page
        if gui_folders.showing:
            if current_folder_page != total_folder_pages:
                current_folder_page += 1
            else:
                current_folder_page = 1

            gui_folders.freeze()

    def file_manager_previous_folder_page():
        """previous_folder_page"""
        global current_folder_page
        if gui_folders.showing:
            if current_folder_page != 1:
                current_folder_page -= 1
            else:
                current_folder_page = total_folder_pages

            gui_folders.freeze()


pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")


def create_spoken_forms(symbols, max_len=30):
    return [" ".join(list(islice(pattern.findall(s), max_len))) for s in symbols]


def get_directory_map(current_path):
    directories = [
        f.name
        for f in islice(
            current_path.iterdir(), settings.get("user.file_manager_folder_limit", 1000)
        )
        if f.is_dir()
    ]
    # print(len(directories))
    spoken_forms = create_spoken_forms(directories)
    return dict(zip(spoken_forms, directories))


def get_file_map(current_path):
    files = [
        f.name
        for f in islice(
            current_path.iterdir(), settings.get("user.file_manager_file_limit", 1000)
        )
        if f.is_file()
    ]
    # print(str(files))
    spoken_forms = create_spoken_forms([p for p in files])
    return dict(zip(spoken_forms, [f for f in files]))


@imgui.open(y=10, x=900, software=False)
def gui_folders(gui: imgui.GUI):
    global current_folder_page, total_folder_pages
    total_folder_pages = math.ceil(
        len(ctx.lists["self.file_manager_directories"]) / setting_imgui_limit.get()
    )
    gui.text(
        "Select a directory ({}/{})".format(current_folder_page, total_folder_pages)
    )
    gui.line()

    index = 1
    current_index = (current_folder_page - 1) * setting_imgui_limit.get()

    while index <= setting_imgui_limit.get() and current_index < len(folder_selections):
        gui.text("{}: {} ".format(index, folder_selections[current_index]))
        current_index += 1
        index = index + 1

    # if total_folder_pages > 1:
    # gui.spacer()

    # if gui.button('Next...'):
    #    actions.user.file_manager_next_folder_page()

    # if gui.button("Previous..."):
    #   actions.user.file_manager_previous_folder_page()


@imgui.open(y=10, x=1300, software=False)
def gui_files(gui: imgui.GUI):
    global file_selections, current_file_page, total_file_pages
    total_file_pages = math.ceil(len(file_selections) / setting_imgui_limit.get())

    gui.text("Select a file ({}/{})".format(current_file_page, total_file_pages))
    gui.line()
    index = 1
    current_index = (current_file_page - 1) * setting_imgui_limit.get()

    while index <= setting_imgui_limit.get() and current_index < len(file_selections):
        gui.text("{}: {} ".format(index, file_selections[current_index]))
        current_index = current_index + 1
        index = index + 1

    # if total_file_pages > 1:
    #    gui.spacer()

    #    if gui.button('Next...'):
    #        actions.user.file_manager_next_file_page()

    #   if gui.button("Previous..."):
    #        actions.user.file_manager_previous_file_page()


def update_lists():
    global folder_selections, file_selections, current_folder_page, current_file_page
    is_valid_path = False
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
        try:
            directories = get_directory_map(current_path)
            files = get_file_map(current_path)
        except:
            directories = {}
            files = {}
        folder_selections = sorted(directories.values(), key=str.casefold)
        file_selections = sorted(files.values(), key=str.casefold)

    current_folder_page = current_file_page = 1

    lists = {
        "self.file_manager_directories": directories,
        "self.file_manager_files": files,
    }
    ctx.lists.update(lists)

    # if we made it this far, either it's showing and we need to force an update
    # or we need to hide the gui
    if gui_folders.showing or setting_auto_show_pickers.get() >= 1:
        gui_folders.freeze()
        gui_files.freeze()


def win_event_handler(window):
    global cached_path

    # on windows, we get events from the clock
    # and such, so this check is important
    if not window.app.exe or window != ui.active_window():
        return

    if not "user.file_manager" in registry.tags:
        if gui_folders.showing:
            gui_folders.hide()
            gui_files.hide()

        if (
            len(ctx.lists["self.file_manager_directories"]) > 0
            or len(ctx.lists["self.file_manager_files"]) > 0
        ):
            lists = {
                "self.file_manager_directories": [],
                "self.file_manager_files": [],
            }
            ctx.lists.update(lists)

        cached_path = None
        return
    else:
        path = actions.user.file_manager_current_path()
        if cached_path != path:
            update_lists()

        cached_path = path


ui.register("win_title", win_event_handler)
ui.register("win_focus", win_event_handler)

