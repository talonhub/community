import subprocess

from talon import Context, Module, actions, settings, ui

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
ctx.tags = [
    "terminal",
    "user.generic_unix_shell",
    "user.file_manager",
    "user.git",
    "user.kubectl",
]

directories_to_remap = {}
directories_to_exclude = {}

mod.setting(
    "cygpath",
    type=str,
    default="C:\\cygwin64\\bin\\cygpath.exe",
    desc="Path to  cygpath.exe",
)


def get_win_path(cyg_path):
    path = ""
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        path = (
            subprocess.check_output(
                [settings.get("user.cygpath"), "-w", cyg_path], startupinfo=si
            )
            .strip(b"\n")
            .decode()
        )
    except:
        path = ""
    return path


@ctx.action_class("edit")
class EditActions:
    def paste():
        actions.key("shift-insert")

    def copy():
        actions.key("ctrl-insert")

    def delete_line():
        actions.key("ctrl-u")


@ctx.action_class("user")
class UserActions:
    def file_manager_open_parent():
        actions.insert("cd ..")
        actions.key("enter")

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
        path = f'"{path}"'
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(path)

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        name = f'"{name}"'

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

    def terminal_list_directories():
        actions.insert("ls")
        actions.key("enter")

    def terminal_list_all_directories():
        actions.insert("ls -a")
        actions.key("enter")

    def terminal_change_directory(path: str):
        actions.insert(f"cd {path}")
        if path:
            actions.key("enter")

    def terminal_change_directory_root():
        """Root of current drive"""
        actions.insert("cd /")
        actions.key("enter")

    def terminal_clear_screen():
        """Clear screen"""
        actions.key("ctrl-l")

    def terminal_run_last():
        actions.key("up enter")

    def terminal_kill_all():
        actions.key("ctrl-c")
        actions.insert("y")
        actions.key("enter")
