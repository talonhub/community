from talon import Context, Module, actions, imgui, settings, ui
import os
import subprocess

mod = Module()
mod.apps.mintty = """
os: windows
and app.name: Terminal
os: windows
and app.name: mintty.exe
"""

ctx = Context()
ctx.matches = r"""
app: mintty
"""
directories_to_remap = {}
directories_to_exclude = {}

setting_cyg_path = mod.setting(
    "cygpath",
    type=str,
    default="C:\\cygwin64\\bin\\cygpath.exe",
    desc="Path to  cygpath.exe",
)


def get_win_path(cyg_path):
    path = ""
    try:
        path = (
            subprocess.check_output([setting_cyg_path.get(), "-w", cyg_path])
            .strip(b"\n")
            .decode()
        )
    except:
        path = ""
    return path


@ctx.action_class("user")
class user_actions:
    def file_manager_current_path():
        path = ui.active_window().title
        path = get_win_path(path)

        if path in directories_to_remap:
            path = directories_to_remap[title]

        if path in directories_to_exclude:
            path = ""
        return path

    def file_manager_show_properties():
        """Shows the properties for the file"""

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.insert("cd ")
        path = '"{}"'.format(path)
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(path)

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        name = '"{}"'.format(name)

        actions.insert("mkdir " + name)

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.insert(path)

    def file_manager_open_volume(volume: str):
        """file_manager_open_volume"""
        actions.user.file_manager_open_directory(volume)
