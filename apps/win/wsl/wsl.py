from talon import Context, Module, actions, imgui, settings, ui, app
import os
import subprocess

mod = Module()
mod.apps.ubuntu = """
os: windows
and app.name: ubuntu.exe
"""

ctx = Context()
ctx.matches = r"""
app: ubuntu
"""
directories_to_remap = {}
directories_to_exclude = {}


def get_win_path(wsl_path):
    path = ""
    try:
        path = (
            subprocess.check_output(["wsl", "wslpath", "-w", wsl_path])
            .strip(b"\n")
            .decode()
        )
    except:
        path = ""

    return path


def get_wsl_path(win_path):
    path = ""
    try:
        path = (
            subprocess.check_output(["wsl", "wslpath", "-u", "'{}'".format(win_path)])
            .strip(b"\n")
            .decode()
        )
    except:
        path = ""

    return path


@ctx.action_class("user")
class user_actions:
    def file_manager_current_path():
        # print("title = " + ui.active_window().title)
        path = ui.active_window().title
        path = get_win_path(path.split(":")[1].lstrip())

        if path in directories_to_remap:
            path = directories_to_remap[path]

        if path in directories_to_exclude:
            path = ""
        # print(path)
        return path

    # def file_manager_terminal_here():
    #     actions.key("ctrl-l")
    #     actions.insert("cmd.exe")
    #     actions.key("enter")

    # def file_manager_show_properties():
    #     """Shows the properties for the file"""
    #     actions.key("alt-enter")
    def file_manager_open_user_directory(path: str):
        """expands and opens the user directory"""
        path = os.path.expanduser(os.path.join("~", path))
        if ":" in path:
            path = get_wsl_path(path)
        # print("after: " + path)

        actions.user.file_manager_open_directory(path)

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

