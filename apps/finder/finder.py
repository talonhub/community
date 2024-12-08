import os

from talon import Context, actions, ui
from talon.mac import applescript

ctx = Context()
ctx.matches = r"""
app: finder
"""
directories_to_remap = {"": "/Volumes"}
directories_to_exclude = {}


@ctx.action_class("user")
class UserActions:
    def file_manager_open_parent():
        actions.key("cmd-up")

    def file_manager_current_path():
        title = ui.active_window().title

        if "~" in title:
            title = os.path.expanduser(title)

        if title in directories_to_remap:
            title = directories_to_remap[title]

        if title in directories_to_exclude:
            title = ""

        return title

    def file_manager_terminal_here():
        applescript.run(
            r"""
        tell application "Finder"
            set myWin to window 1
            set thePath to (quoted form of POSIX path of (target of myWin as alias))
            tell application "Terminal"
                activate
                tell window 1
                    do script "cd " & thePath
                end tell
            end tell
        end tell"""
        )

    def file_manager_show_properties():
        """Shows the properties for the file"""
        actions.key("cmd-i")

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.key("cmd-shift-g")
        actions.sleep("50ms")
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(path)

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        actions.key("cmd-shift-n")
        actions.insert(name)

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.key("home")
        actions.insert(path)
        actions.key("cmd-o")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.key("home")
        actions.insert(path)

    def address_focus():
        actions.key("cmd-shift-g")

    def address_copy_address():
        actions.key("alt-cmd-c")

    def address_navigate(address: str):
        actions.user.file_manager_open_directory(address)
