import os

from talon import Context, Module, actions, app, ui

mod = Module()
apps = mod.apps

apps.windows_explorer = """
os: windows
and app.name: Windows Explorer
os: windows
and app.name: Windows-Explorer
os: windows
and app.exe: /explorer.exe/i
"""

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
app: windows_explorer
app: windows_file_browser
"""

user_path = os.path.expanduser("~")
directories_to_remap = {}
directories_to_exclude = {}

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

    if nameBuffer.value:
        directories_to_remap[nameBuffer.value] = user_path

    directories_to_exclude = [
        "",
        "Run",
        "Task Switching",
        "Task View",
        "This PC",
        "File Explorer",
        "Program Manager",
    ]


@ctx.action_class("user")
class UserActions:
    def file_manager_go_back():
        actions.key("alt-left")

    def file_manager_go_forward():
        actions.key("alt-right")

    def file_manager_open_parent():
        actions.key("alt-up")

    def file_manager_current_path():
        path = ui.active_window().title

        if path in directories_to_remap:
            path = directories_to_remap[path]

        if path in directories_to_exclude:
            actions.user.file_manager_hide_pickers()
            path = ""

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
