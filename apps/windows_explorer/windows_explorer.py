import os
import win32com.client
import win32gui

from talon import Context, Module, actions, app, ui
from ...core.operating_system.windows.windows_known_paths import resolve_known_windows_path, FOLDERID

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
  
    known_paths_to_resolve = {
        "Desktop": FOLDERID.Desktop,
        "Documents": FOLDERID.Documents,
        "Downloads": FOLDERID.Documents,
        "Music": FOLDERID.Music,
        "Pictures": FOLDERID.Pictures,
        "Videos": FOLDERID.Profile
    }

    for key, value in known_paths_to_resolve.items():
        try:
            path = resolve_known_windows_path(value)
        except Exception as e:
            path = None

    directories_to_exclude = [
        "",
        "Run",
        "Task Switching",
        "Task View",
        "This PC",
        "File Explorer",
        "Program Manager",
    ]

def get_active_explorer_path():
    shell = win32com.client.Dispatch("Shell.Application")
    hwnd = win32gui.GetForegroundWindow()

    for window in shell.Windows():
        try:
            if window.HWND == hwnd:
                return window.Document.Folder.Self.Path
        except Exception:
            continue

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
        actions.sleep("100ms")
        actions.insert(path)
        actions.sleep("100ms")
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
        actions.sleep("50ms")
        actions.insert(path)
        actions.sleep("50ms")
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
        actions.sleep("100ms")
        actions.edit.copy()

    def address_navigate(address: str):
        actions.user.file_manager_open_directory(address)
