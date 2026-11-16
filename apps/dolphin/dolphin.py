from pathlib import Path

from talon import Context, Module, actions, ui

# Dolphin is the default file manager for KDE plasma, one of
# the two biggest linux desktop environments.
mod = Module()
mod.apps.dolphin = """
os: linux
and app.name: dolphin
"""

# Context matching
ctx = Context()
ctx.matches = r"""
app: dolphin
"""


@ctx.action_class("user")
class UserActions:
    # user.tabs
    def tab_jump(number: int):
        actions.key(f"alt-{number}")

    # user.navigation
    def go_back():
        actions.key("alt-left")

    def go_forward():
        actions.key("alt-right")

    def file_manager_open_parent():
        actions.key("alt-up")

    def file_manager_current_path() -> str:
        """Returns the current path for the active file manager."""
        title = ui.active_window().title
        if not title:
            return ""

        # Dolphin appends " — Dolphin" or " - Dolphin" to window titles
        for suffix in (" — Dolphin", " - Dolphin"):
            if title.endswith(suffix):
                title = title.removesuffix(suffix)
                break

        if not Path(title).is_absolute():
            actions.user.debounce_notify(
                "dolphin_full_path_title",
                'Enable "Show full path in title bar" in Dolphin settings to use file manager commands.',
            )
            return ""

        return title

    def file_manager_terminal_here():
        """Opens terminal at current location"""
        actions.key("f4")

    def file_manager_show_properties():
        """Shows the properties for the file"""
        actions.key("alt-enter")

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.user.address_focus()
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(path)

    def file_manager_new_folder(name: str = ""):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        actions.key("f10")
        if name:
            actions.insert(name)
            actions.key("enter")

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

    # user.address
    def address_focus():
        actions.key("ctrl-l")

    def address_copy_address():
        actions.user.address_focus()
        actions.edit.copy()
        actions.key("escape")

    def address_navigate(address: str):
        actions.user.file_manager_open_directory(address)
