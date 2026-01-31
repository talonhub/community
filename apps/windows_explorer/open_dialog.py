import os
import win32com.client
import win32gui

from talon import Context, Module, actions, app, ui, clip
from ...core.operating_system.windows.windows_known_paths import resolve_known_windows_path, FOLDERID

mod = Module()
apps = mod.apps


# many commands should work in most save/open dialog.
# note the "show options" stuff won't work unless work
# unless the path is displayed in the title, which is rare for those
apps.windows_file_browser = """
os: windows
and app.name: /.*/
and title: /(Save|Open|Browse|Select)/
"""

ctx = Context()
ctx.matches = r"""
win.class: #32770
"""


def get_active_explorer_path():
    try: 
        toolbar = ui.active_window().element.find_one(automation_id = "1001", max_depth=0)
        if toolbar:
            path = toolbar.legacyiaccessible_pattern.name.replace("Address: ", "")
            return path
        else:
            print("didn't find toolbar")
    except:
        pass

    return None

@ctx.action_class("user")
class UserActions:
    def file_manager_open_parent():
        actions.key("alt-up")

    def file_manager_current_path():
        path = get_active_explorer_path()

        # if path in directories_to_remap:
        #     path = directories_to_remap[path]

        # if path in directories_to_exclude:
        #     actions.user.file_manager_hide_pickers()
        #     path = ""

        return path

    def file_manager_terminal_here():
        actions.key("ctrl-l")
        actions.insert("cmd.exe")
        actions.key("enter")

    def file_manager_show_properties():
        """Shows the properties for the file"""
        actions.key("alt-enter")

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.key("ctrl-l")
        toolbar = ui.active_window().element.find_one(automation_id = "1001", max_depth=0)
        toolbar.value_pattern.value = path
        actions.key("enter")

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(path)

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        actions.key("home")
        actions.key("ctrl-shift-n")
        actions.insert(name)

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.key("ctrl-l")
        toolbar = ui.active_window().element.find_one(automation_id = "1001", max_depth=0)
        toolbar.value_pattern.value = path
        actions.key("enter")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.key("home")
        actions.insert(path)

    def file_manager_open_volume(volume: str):
        """file_manager_open_volume"""
        actions.user.file_manager_open_directory(volume)

    def address_focus():
        actions.key("ctrl-l")

    def address_copy_address():
        path = get_active_explorer_path()
        if path:
            clip.set_text(path)

    def address_navigate(address: str):
        actions.user.file_manager_open_directory(address)
