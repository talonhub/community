from talon import app, Module, Context, actions, ui, imgui, registry
from os.path import expanduser
from subprocess import Popen
from pathlib import Path
from typing import List, Union
from . import utils
import os
import math
import platform

platform = platform.platform(terse=True)
#print("platform = " + platform)
selection_numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',]
selection_map = {n: i for i, n in enumerate(selection_numbers)}

mod = Module()
mod.list('file_manager_directory_index', desc='number -> directory name')
mod.list('file_manager_file_index', desc='number -> file name')
mod.list('file_manager_directory_remap', desc='list of titles remapped to the absolute path')
mod.list('file_manager_directory_exclusions', desc='list of titles that are excluded/disabled from the picker functionality')
mod.setting('file_manager_auto_show_pickers', 'int')

ctx = Context()
ctx.settings["user.file_manager_auto_show_pickers"] = 1

user_path = os.path.expanduser('~')

folder_selections = []
file_selections = []

is_windows = False
is_mac = False
is_terminal = False
is_linux = False

if "Windows-10" in platform:
    is_windows = True
    import ctypes
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3

    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)

    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, nameBuffer, size)

    #todo use expanduser for cross platform support
    ctx.lists['user.file_manager_directory_remap'] = {
        "Desktop": os.path.join(user_path, "Desktop"),
        "Downloads": os.path.join(user_path, "Downloads"),
        "Documents": os.path.join(user_path, "Documents"),
        "Pictures": os.path.join(user_path, "Pictures"),
        "Music": os.path.join(user_path, "Music"),
    }

    ctx.lists['user.file_manager_directory_remap'][nameBuffer.value] = user_path
    ctx.lists['user.file_manager_directory_exclusions'] = [
    "Run",
    "Task View",
    "",
    "Task Switching",
]
    supported_programs = ["explorer.exe", "cmd.exe",]
    terminal_programs = ["cmd.exe"]

elif "Darwin" in platform:
    ###
    #print("Mac OS X!!")
    is_mac = True
    ctx.lists['user.file_manager_directory_remap'] = {}
    ctx.lists['user.file_manager_directory_exclusions'] = {}
    supported_programs = ["com.apple.Terminal", "com.apple.finder"]
    terminal_programs = ["com.apple.Terminal",]

elif "linux" in platform.lower():
    is_linux = True
    ctx.lists['user.file_manager_directory_remap'] = {}
    ctx.lists['user.file_manager_directory_exclusions'] = {}
    supported_programs = ['Caja']
    terminal_programs = ['terminal']

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

    def file_manager_show_pickers():
        """Shows the pickers"""
        global is_showing
        is_showing = True
        gui_files.show()
        gui_folders.show()

    def file_manager_hide_pickers():
        """Hides the pickers"""
        global is_showing
        is_showing = False
        gui_files.hide()
        gui_folders.hide()

    def file_manager_open_file(path: Union[str, int]):
        """opens the file"""
        #if is_showing:
        if is_windows:
            actions.key("home")
            if isinstance(path, int):
                actions.insert(m[path])
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
        #if is_showing:
        actions.key("home")
        if isinstance(path, int):
            #print(str(file_selections))
            #print('select file = ' + str(path) + ' ' + file_selections[path])
            actions.insert(file_selections[path])
        else:
            actions.insert(path)

    def file_manager_refresh_title():
        """Refreshes the title to match current directory"""
        return
        #todo: this is for e.g. windows command prompt that will need to do some magic.

    def file_manager_next_file_page():
        """next_file_page"""
        global current_file_page
        if current_file_page != total_file_pages:
            current_file_page += 1
        else:
            current_file_page = 1

    def file_manager_previous_file_page():
        """previous_file_page"""
        global current_file_page
        if current_file_page != 1:
            current_file_page -= 1
        else:
            current_file_page = total_file_pages

    def file_manager_next_folder_page():
        """next_folder_page"""
        global current_folder_page
        if is_showing:
            if current_folder_page != total_folder_pages:
                current_folder_page += 1
            else:
                current_folder_page = 1

    def file_manager_previous_folder_page():
        """previous_folder_page"""
        global current_folder_page
        if is_showing:
            if current_folder_page != 1:
                current_folder_page -= 1
            else:
                current_folder_page = total_folder_pages

    def file_manager_terminal_open_directory(path: Union[str, int]):
        """file_manager_terminal_open_directory TODO: remove once we can implement that take parameters in .talon"""
        actions.insert("cd ")
        if isinstance(path, int):
            actions.insert(folder_selections[path])
        else:
            actions.insert(path)

        actions.key("enter")
        actions.user.file_manager_refresh_title()

    def file_manager_open_user_directory(path: str):
        """expands and opens the user directory"""
        path = os.path.expanduser(os.path.join('~', path))
        actions.user.file_manager_open_directory(path)

    def file_manager_open_directory(path: Union[str, int]):
        """opens the directory that's already visible in the view"""
        if is_terminal:
            actions.user.file_manager_terminal_open_directory(path)
        else:
            if is_windows:
                actions.key("ctrl-l")
                if isinstance(path, int):
                    actions.insert(folder_selections[path])
                else:
                    actions.insert(path)

                actions.key("enter")
            elif is_mac:
                actions.key("cmd-shift-g")
                actions.sleep("50ms")
                if isinstance(path, int):
                    actions.insert(folder_selections[path])
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
            actions.insert(folder_selections[path])
        else:
            actions.insert(path)

path_last_update = None
is_showing = False

def update_maps(window):
    global path_last_update, is_showing, folder_selections, file_selections, current_folder_page, current_file_page, is_terminal
    #print("app: " + str(window.app))
    #print("app: " + str(window.app.bundle))
    #print("title: " + str(window.title))
    #print("ui.active_window().doc: ")
    if not window.app.exe or window.title != ui.active_window().title:
        return
    title = window.title

    if title in registry.lists['user.file_manager_directory_remap'][0]:
        title = registry.lists['user.file_manager_directory_remap'][0][title]

    is_supported = False
    is_terminal = False
    
    for item in supported_programs:
        if is_windows:
            if item in window.app.exe.lower():
                is_supported = True
                break
        elif is_mac:
            if item in window.app.bundle:
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

    if not is_supported or title in registry.lists["user.file_manager_directory_exclusions"][0] or not title or title == "":
        ctx.lists["self.file_manager_directories"] = []
        ctx.lists["self.file_manager_files"] = []
        path_last_update = None
        is_showing = False
        is_terminal = False
        gui_folders.hide()
        gui_files.hide()
        return

    if is_mac and "~" in title:
        title = os.path.expanduser(title)

    current_path = Path(title)
    if not current_path.is_dir():
        return
    path_last_update = current_path
    
    ctx.lists["self.file_manager_directories"] = utils.get_directory_map(current_path)
    ctx.lists["self.file_manager_files"] = utils.get_file_map(current_path)

    index = 1
    folder_selections = []
    for path in sorted (ctx.lists["self.file_manager_directories"].values(), key=str.casefold):  
        folder_selections.append(path)
        index = index + 1 
    
    ctx.lists['self.file_manager_directory_index'] = selection_numbers[:index-1]

    index = 1
    file_selections = []
    for path in sorted (ctx.lists["self.file_manager_files"].values(), key=str.casefold):  
        #print("path = " + path)
        file_selections.append(path)
        index = index + 1 
    
    ctx.lists['self.file_manager_file_index'] = selection_numbers[:index-1]
    current_folder_page = current_file_page = 1

    #print(str(ctx.lists["self.directories"]))
    #print(str(ctx.lists["self.files"]))
    #print("Show pickers: " + str(registry.settings["user.auto_show_pickers"]))
    if not is_showing and registry.settings["user.file_manager_auto_show_pickers"][1] >= 1:
        is_showing = True

        gui_folders.show()
        gui_files.show()

ui.register("win_title", update_maps)
ui.register("win_focus", update_maps)

ctx.lists["self.file_manager_directories"] = []
ctx.lists['self.file_manager_directory_index'] = []
ctx.lists["self.file_manager_files"] = []
ctx.lists['self.file_manager_file_index'] = []

@ctx.capture(rule='{self.file_manager_directories}')
def file_manager_directories(m):
    return m.file_manager_directories

@ctx.capture(rule='{self.file_manager_directory_index}')
def file_manager_directory_index(m):
    current_index = (current_folder_page - 1) * len(selection_numbers) + selection_map[m.file_manager_directory_index] 
    return folder_selections[current_index]

@ctx.capture(rule='{self.file_manager_files}')
def file_manager_files(m):
    return m.file_manager_files

@ctx.capture(rule='{self.file_manager_file_index}')
def file_manager_file_index(m):
    current_index = (current_folder_page - 1) * len(selection_numbers) + selection_map[m.file_manager_file_index]
    return file_selections[current_index]

current_folder_page = 1
@imgui.open(y=10,x=900)
def gui_folders(gui: imgui.GUI):
    global current_folder_page, total_folder_pages
    total_folder_pages = math.ceil(len(ctx.lists["self.file_manager_directories"]) / len(selection_numbers))
    gui.text("Select a directory ({}/{})".format(current_folder_page, total_folder_pages))
    gui.line()

    index = 1
    current_index = (current_folder_page - 1) * len(selection_numbers)

    while index <= len(selection_numbers) and current_index < len(folder_selections):
        gui.text("{}: {} ".format(index, folder_selections[current_index]))
        current_index += 1
        index = index + 1

    if total_folder_pages > 1:
        gui.spacer()
        
        if gui.button('Next...'):
            actions.user.file_manager_next_folder_page()

        if gui.button("Previous..."):
            actions.user.file_manager_previous_folder_page()

current_file_page = 1
@imgui.open(y=10,x=1300)
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

    if total_file_pages > 1:
        gui.spacer()

        if gui.button('Next...'):
            actions.user.file_manager_next_file_page()

        if gui.button("Previous..."):
            actions.user.file_manager_previous_file_page()

