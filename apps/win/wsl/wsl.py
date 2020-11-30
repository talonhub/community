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
app: windows_terminal
and win.title: /Ubuntu/ 
"""
directories_to_remap = {}
directories_to_exclude = {}

user_path = os.path.expanduser("~")
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

        directories_to_remap = {
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
        directories_to_remap = {
            "Desktop": os.path.join(user_path, "Desktop"),
            "Documents": os.path.join(user_path, "Documents"),
            "Downloads": os.path.join(user_path, "Downloads"),
            "Music": os.path.join(user_path, "Music"),
            "OneDrive": one_drive_path,
            "Pictures": os.path.join(user_path, "Pictures"),
            "Videos": os.path.join(user_path, "Videos"),
        }


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


def get_usr_path():
    path = ""
    try:
        path = (
            subprocess.check_output(["wsl", "wslpath", "-a", "~"]).strip(b"\n").decode()
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
    def file_manager_refresh_title():
        actions.skip()

    def file_manager_current_path():
        path = ui.active_window().title
        try:
            path = path.split(":")[1].lstrip()
        except:
            path = ""

        # print("current: " + path)
        if "~" in path:
            # the only way I could find to correctly support the user folder:
            # get absolute path of ~, and strip /mnt/x from the string
            abs_usr_path = get_usr_path()
            abs_usr_path = abs_usr_path[abs_usr_path.find("/home") : len(abs_usr_path)]
            path = path.replace("~", abs_usr_path)

        path = get_win_path(path)

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
    def file_manager_open_user_directory(path: str):
        """expands and opens the user directory"""
        if path in directories_to_remap:
            path = directories_to_remap[path]

        path = os.path.expanduser(os.path.join("~", path))
        if ":" in path:
            path = get_wsl_path(path)

        actions.user.file_manager_open_directory(path)

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        if ":" in str(path):
            path = get_wsl_path(path)

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

