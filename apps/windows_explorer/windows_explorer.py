import os

from talon import Context, Module, actions, app, ui
from .explorer_path import get_active_explorer_path

mod = Module()
apps = mod.apps

apps.windows_explorer = r"""
os: windows
and app.name: Windows Explorer
os: windows
and app.name: Windows-Explorer
os: windows
and app.exe: /^explorer\.exe$/i
"""
ctx = Context()
ctx.matches = r"""
app: windows_explorer
"""

@ctx.action_class("user")
class UserActions:
    def file_manager_open_parent():
        actions.key("alt-up")

    def file_manager_current_path():
        path = get_active_explorer_path()

        if path.is_virtual:
            # note:  possibly explore whether we can do anything useful with these folders via accessibility
            actions.app.notify("Cannot get path for virtual folder, command skipped")
            return None
        else:
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
        actions.insert(path)
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
        actions.key("home")
        actions.insert(path)
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
        actions.key("ctrl-l")
        actions.edit.copy()

    def address_navigate(address: str):
        actions.user.file_manager_open_directory(address)
