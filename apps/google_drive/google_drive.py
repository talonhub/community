from talon import Context, Module, actions

mod = Module()

# Match the web application running in any browser by tab title
mod.apps.google_drive = r"""
tag: browser
browser.host: drive.google.com
"""

ctx = Context()
ctx.matches = r"""
app: google_drive
"""


@ctx.action_class("user")
class UserActions:
    # user.file_manager
    def file_manager_open_parent():
        actions.key("alt-up")

    def file_manager_show_properties():
        actions.key("d")

    def file_manager_open_directory(path: str):
        # Jump to Drive search bar and submit query
        actions.key("/")
        actions.insert(path)
        actions.key("enter")

    def file_manager_new_folder(name: str = None):
        actions.key("shift-f")
        if name:
            actions.sleep("200ms")
            actions.insert(name)
            actions.key("enter")
