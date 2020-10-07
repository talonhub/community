from talon import app, Module, Context, actions, ui, imgui, settings, app
from os.path import expanduser
from subprocess import Popen
from pathlib import Path
from typing import List, Union
import os
import math
import re
from itertools import islice

selection_numbers = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
]
selection_map = {n: i for i, n in enumerate(selection_numbers)}

mod = Module()
ctx = Context()

mod.list(
    "file_manager_directory_remap", desc="list of titles remapped to the absolute path"
)
mod.list(
    "file_manager_directory_exclusions",
    desc="list of titles that are excluded/disabled from the picker functionality",
)
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
mod.tag("file_manager", desc="Tag for enabling generic file management commands")

user_path = os.path.expanduser("~")

folder_selections = []
file_selections = []

is_windows = False
is_mac = False
is_terminal = False
is_linux = False
cached_title = None

if app.platform == "windows":
    is_windows = True
    import ctypes

    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3

    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)

    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, nameBuffer, size)
    one_drive_path = os.path.expanduser(os.path.join("~", "OneDrive"))

    # this is probably not the correct way to check for onedrive, quick and dirty
    if os.path.isdir(os.path.expanduser(os.path.join("~", r"OneDrive\Desktop"))):
        default_folder = os.path.join("~", "Desktop")

        ctx.lists["user.file_manager_directory_remap"] = {
            "Desktop": os.path.join(one_drive_path, "Desktop"),
            "Documents": os.path.join(one_drive_path, "Documents"),
            "Downloads": os.path.join(user_path, "Downloads"),
            "Music": os.path.join(user_path, "Music"),
            "OneDrive": one_drive_path,
            "Pictures": os.path.join(one_drive_path, "Pictures"),
            "Videos": os.path.join(user_path, "Videos"),
        }
    else:
        # todo use expanduser for cross platform support
        ctx.lists["user.file_manager_directory_remap"] = {
            "Desktop": os.path.join(user_path, "Desktop"),
            "Documents": os.path.join(user_path, "Documents"),
            "Downloads": os.path.join(user_path, "Downloads"),
            "Music": os.path.join(user_path, "Music"),
            "OneDrive": one_drive_path,
            "Pictures": os.path.join(user_path, "Pictures"),
            "Videos": os.path.join(user_path, "Videos"),
        }

    if nameBuffer.value:
        ctx.lists["user.file_manager_directory_remap"][nameBuffer.value] = user_path

    ctx.lists["user.file_manager_directory_exclusions"] = [
        "",
        "Run",
        "Task Switching",
        "Task View",
        "This PC",
        "File Explorer",
    ]
    supported_programs = [
        "cmd.exe",
        "explorer.exe",
    ]
    terminal_programs = ["cmd.exe"]

elif app.platform == "mac":
    ###
    # print("Mac OS X!!")
    is_mac = True
    ctx.lists["user.file_manager_directory_remap"] = {"": "/Volumes"}
    ctx.lists["user.file_manager_directory_exclusions"] = {}
    supported_programs = ["com.apple.Terminal", "com.apple.finder"]
    terminal_programs = [
        "com.apple.Terminal",
    ]

elif app.platform == "linux":
    is_linux = True
    ctx.lists["user.file_manager_directory_remap"] = {}
    ctx.lists["user.file_manager_directory_exclusions"] = {}
    supported_programs = ["Caja", "terminal"]
    terminal_programs = ["terminal"]


@mod.capture
def file_manager_directories(m) -> str:
    "Returns a single string"


@mod.capture
def file_manager_files(m) -> str:
    "Returns the selected file"


@mod.capture
def file_manager_directory_index(m) -> int:
    "Directory selection index"


@mod.capture
def file_manager_file_index(m) -> int:
    "File selection index"


@mod.action_class
class Actions:
    def file_manager_open_parent():
        """file_manager_open_parent"""
        return

    def file_manager_go_forward():
        """file_manager_go_forward_directory"""

    def file_manager_go_back():
        """file_manager_go_forward_directory"""

    def file_manager_toggle_pickers():
        """Shows the pickers"""

        if gui_files.showing:
            gui_files.hide()
            gui_folders.hide()
        else:
            gui_files.freeze()
            gui_folders.freeze()

    def file_manager_hide_pickers():
        """Hides the pickers"""
        gui_files.hide()
        gui_folders.hide()

    def file_manager_open_file(path: Union[str, int]):
        """opens the file"""
        if is_windows:
            # print("file_manager_open_file")
            actions.key("home")
            if isinstance(path, int):
                index = (current_file_page - 1) * len(selection_numbers) + path
                if path < len(file_selections):
                    actions.insert(file_selections[index])
            else:
                actions.insert(path)

            actions.key("enter")
        elif is_mac:
            actions.key("home")
            if isinstance(path, int):
                actions.insert(m[path])
            else:
                actions.insert(path)
            actions.key("cmd-o")

    def file_manager_select_file(path: Union[str, int]):
        """selects the file"""
        actions.key("home")
        if isinstance(path, int):
            # print(str(file_selections))
            # print('select file = ' + str(path) + ' ' + file_selections[path])
            index = (current_file_page - 1) * len(selection_numbers) + path
            if index < len(file_selections):
                actions.insert(file_selections[index])
        else:
            actions.insert(path)

    def file_manager_refresh_title():
        """Refreshes the title to match current directory"""
        return
        # todo: this is for e.g. windows command prompt that will need to do some magic.

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

    def file_manager_open_volume(volume: str):
        """file_manager_open_volume"""
        if is_windows:
            if is_terminal:
                actions.insert(volume)
                actions.key("enter")
                actions.user.file_manager_refresh_title()
            else:
                actions.user.file_manager_open_directory(volume)
        # todo: mac etc

    def file_manager_terminal_open_directory(path: Union[str, int]):
        """file_manager_terminal_open_directory TODO: remove once we can implement that take parameters in .talon"""
        actions.insert("cd ")
        if isinstance(path, int):
            index = (current_folder_page - 1) * len(selection_numbers) + path
            if index < len(folder_selections):
                actions.insert('"{}"'.format(folder_selections[index]))
        else:
            actions.insert(path)

        actions.key("enter")
        actions.user.file_manager_refresh_title()

    def file_manager_open_user_directory(path: str):
        """expands and opens the user directory"""
        path = os.path.expanduser(os.path.join("~", path))
        actions.user.file_manager_open_directory(path)

    def file_manager_open_directory(path: Union[str, int]):
        """opens the directory that's already visible in the view"""
        if is_terminal:
            actions.user.file_manager_terminal_open_directory(path)
        else:

            if is_windows:
                actions.key("ctrl-l")
                if isinstance(path, int):
                    index = (current_folder_page - 1) * len(selection_numbers) + path
                    if index < len(folder_selections):
                        actions.insert(folder_selections[index])
                else:
                    actions.insert(path)

                actions.key("enter")
            elif is_mac:
                actions.key("cmd-shift-g")
                actions.sleep("50ms")
                if isinstance(path, int):
                    index = (current_folder_page - 1) * len(selection_numbers) + path
                    if index < len(folder_selections):
                        actions.insert(folder_selections[index])
                else:
                    actions.insert(path)
                actions.key("enter")
            elif is_linux:
                actions.key("ctrl-l")
                actions.insert(path)
                actions.key("enter")

    def file_manager_select_directory(path: Union[str, int]):
        """selects the directory"""
        if is_windows and not is_terminal:
            actions.key("home")

        if isinstance(path, int):
            index = (current_folder_page - 1) * len(selection_numbers) + path
            if index < len(folder_selections):
                actions.insert(folder_selections[index])
        else:
            actions.insert(path)

    def file_manager_new_folder():
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        if is_windows:
            if is_terminal:
                actions.insert("mkdir ")
            else:
                actions.key("ctrl-shift-n")
        elif is_mac:
            if is_terminal:
                actions.insert("mkdir ")
            else:
                actions.key("cmd-shift-n")
        # tbd
        # else is_linux:

    def file_manager_show_properties():
        """Shows the properties for the file"""
        # todo: does this make sense for terminals? also, linux support
        if not is_terminal:
            if is_windows:
                actions.key("alt-enter")
            elif is_mac:
                actions.key("cmd-i")
            # else:

    def file_manager_terminal_here():
        """Opens terminal at current location"""
        if not is_terminal:
            if is_windows:
                actions.key("ctrl-l")
                actions.insert("cmd.exe")
                actions.key("enter")
            elif is_mac:
                from talon import applescript

                applescript.run(
                    r"""
                tell application "Finder"
                    set myWin to window 1
                    set thePath to (quoted form of POSIX path of (target of myWin as alias))
                    tell application "Terminal"
                        activate
                        tell window 1
                            do script "cd " & thePath
                        end tell
                    end tell
                end tell"""
                )


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


def update_maps(window):
    global is_showing, folder_selections, file_selections, current_folder_page, current_file_page, is_terminal, cached_title
    if (
        not window.app.exe
        or window != ui.active_window()
        or window.title == cached_title
    ):
        return

    title = window.title
    cached_title = title

    directories = {}
    files = {}
    folder_selections = []
    file_selections = []

    is_supported = False
    is_terminal = False
    is_valid_path = False

    for item in supported_programs:
        if is_windows:
            if item in window.app.exe.lower():
                is_supported = True
                break
        elif is_mac:
            if item in window.app.bundle:
                is_supported = True
                break
        elif is_linux:
            if item in window.app.name:
                is_supported = True
                break
    for item in terminal_programs:
        if is_windows:
            if item in window.app.exe.lower():
                is_terminal = True
                break
        elif is_mac:
            if item in window.app.bundle:
                is_terminal = True
                break
        elif is_linux:
            if item in window.app.name:
                is_terminal = True

    if is_windows and is_terminal:
        # if cmd or windows terminal is running as admin...
        # strip it
        title = title.replace("Administrator:  ", "")
        # print("title: " + title)
    excluded_path = False
    if title in ctx.lists["self.file_manager_directory_remap"]:
        title = ctx.lists["self.file_manager_directory_remap"][title]

    elif title in ctx.lists["self.file_manager_directory_exclusions"]:
        excluded_path = True

        # set valid path to force an update
        is_valid_path = True

    if not is_supported or excluded_path or not title or title == "":
        is_terminal = False
    else:
        if is_mac and "~" in title:
            title = os.path.expanduser(title)

        # Handle hostname before path
        if is_linux and ":" in title:
            title = title.split(":")[1].strip()
            title = os.path.expanduser(title)

        try:
            current_path = Path(title)
            is_valid_path = current_path.is_dir()
        except:
            is_supported = False

        if is_valid_path:
            try:
                directories = get_directory_map(current_path)
                files = get_file_map(current_path)
            except Exception as e:
                directories = {"ERROR": str(e)}
                files = {"ERROR": str(e)}

            folder_selections = sorted(directories.values(), key=str.casefold)
            file_selections = sorted(files.values(), key=str.casefold)

        current_folder_page = current_file_page = 1

    lists = {
        "user.file_manager_directories": directories,
        "user.file_manager_files": files,
    }

    # batch update lists for performance
    ctx.lists.update(lists)

    # if we made it this far, either it's showing and we need to force an update
    # or we need to hide the gui
    if not is_supported:
        if gui_folders.showing:
            gui_folders.hide()
            gui_files.hide()
    elif is_valid_path and (
        gui_folders.showing
        or settings.get("user.file_manager_auto_show_pickers", 0) >= 1
    ):
        gui_folders.freeze()
        gui_files.freeze()

    # todo: figure out what changed in 1320
    # print("hiding: is_valid_path {}, gui_folders.showing {}, title  {}".format(str(is_valid_path), str(gui_folders.showing), str(cached_title)))


ui.register("win_title", update_maps)
ui.register("win_focus", update_maps)

ctx.lists["self.file_manager_directories"] = []
ctx.lists["self.file_manager_files"] = []


@ctx.capture(rule="{self.file_manager_directories}")
def file_manager_directories(m):
    return m.file_manager_directories


@ctx.capture(rule="{self.file_manager_files}")
def file_manager_files(m):
    return m.file_manager_files


current_folder_page = 1


@imgui.open(y=10, x=900, software=False)
def gui_folders(gui: imgui.GUI):
    global current_folder_page, total_folder_pages
    total_folder_pages = math.ceil(
        len(ctx.lists["self.file_manager_directories"]) / len(selection_numbers)
    )
    gui.text(
        "Select a directory ({}/{})".format(current_folder_page, total_folder_pages)
    )
    gui.line()

    index = 1
    current_index = (current_folder_page - 1) * len(selection_numbers)

    while index <= len(selection_numbers) and current_index < len(folder_selections):
        gui.text("{}: {} ".format(index, folder_selections[current_index]))
        current_index += 1
        index = index + 1

    # if total_folder_pages > 1:
    # gui.spacer()

    # if gui.button('Next...'):
    #    actions.user.file_manager_next_folder_page()

    # if gui.button("Previous..."):
    #   actions.user.file_manager_previous_folder_page()


current_file_page = 1


@imgui.open(y=10, x=1300, software=False)
def gui_files(gui: imgui.GUI):
    global file_selections, current_file_page, total_file_pages
    total_file_pages = math.ceil(len(file_selections) / len(selection_numbers))

    gui.text("Select a file ({}/{})".format(current_file_page, total_file_pages))
    gui.line()
    index = 1
    current_index = (current_file_page - 1) * len(selection_numbers)

    while index <= len(selection_numbers) and current_index < len(file_selections):
        gui.text("{}: {} ".format(index, file_selections[current_index]))
        current_index = current_index + 1
        index = index + 1

    # if total_file_pages > 1:
    #    gui.spacer()

    #    if gui.button('Next...'):
    #        actions.user.file_manager_next_file_page()

    #   if gui.button("Previous..."):
    #        actions.user.file_manager_previous_file_page()

