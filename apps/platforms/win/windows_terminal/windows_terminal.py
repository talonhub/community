from talon import Context, Module, actions, imgui, settings, ui, app

import os

ctx = Context()
mod = Module()
ctx.matches = r"""
app: windows_terminal
"""

user_path = os.path.expanduser("~")
directories_to_remap = {}
directories_to_exclude = {}

@ctx.action_class('app')
class AppActions:
    def tab_close(): actions.key('ctrl-shift-w')
    def tab_open():  actions.key('ctrl-shift-t')


@ctx.action_class('edit')
class EditActions:
    def paste(): actions.key('ctrl-shift-v')
    def copy():  actions.key('ctrl-shift-c')
    def find(text: str = None):
        actions.key('ctrl-shift-f')
        if text:
            actions.insert(text)

@ctx.action_class("user")
class UserActions:
    def file_manager_current_path():
        path = ui.active_window().title
        path = (
            path.replace("Administrator:  ", "")
            .replace("Windows PowerShell: ", "")
            .replace("Command Prompt: ", "")
        )

        if path in directories_to_remap:
            path = directories_to_remap[path]

        if path in directories_to_exclude:
            path = ""
        return path

    # def file_manager_terminal_here():
    #     actions.key("ctrl-l")
    #     actions.insert("cmd.exe")
    #     actions.key("enter")

    # def file_manager_show_properties():
    #     """Shows the properties for the file"""
    #     actions.key("alt-enter")

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.insert('cd "{}"'.format(path))
        actions.key("enter")
        actions.user.file_manager_refresh_title()

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert('"{}"'.format(path))

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        actions.insert('mkdir "{}"'.format(name))

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.insert(path)
        # actions.key("enter")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.insert(path)

    def file_manager_open_volume(volume: str):
        """file_manager_open_volume"""
        actions.user.file_manager_open_directory(volume)
        actions.user.file_manager_refresh_title()

    def tab_jump(number: int):
        actions.key("ctrl-alt-{}".format(number))

    def tab_final():
        actions.key("ctrl-alt-9")
