from talon import Context, Module, actions, clip, ui

# App definition. Dolphin is the default file manager for KDE plasma, one of
# the two biggest linux desktop environments.
mod = Module()
mod.apps.dolphin = """
os: linux
and app: dolphin
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

    # user.file_manager
    def file_manager_open_parent():
        actions.key("alt-up")

    def file_manager_show_properties():
        actions.key("alt-enter")

    def file_manager_open_directory(path: str):
        actions.key("ctrl-l")
        actions.insert(path)
        actions.key("enter")

    def file_manager_new_folder(name: str = None):
        actions.key("ctrl-shift-n")
        if name:
            actions.insert(name)

    def file_manager_terminal_here():
        actions.key("alt-shift-f4")
