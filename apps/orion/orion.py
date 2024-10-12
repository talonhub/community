from talon import Context, Module, actions, ui
from talon.mac import applescript

ctx = Context()
mod = Module()
apps = mod.apps
mod.apps.orion = """
os: mac
app.bundle: com.kagi.kagimacOS
"""

ctx.matches = r"""
app: orion
"""


@ctx.action_class("user")
class UserActions:
    def browser_open_address_in_new_tab():
        actions.key("cmd-enter")


@ctx.action_class("browser")
class BrowserActions:
    def bookmark_tabs():
        raise NotImplementedError("Orion doesn't have a default shortcut for this")

    def show_clear_cache():
        actions.key("cmd-alt-e")

    def reload_hard():
        actions.key("cmd-alt-r")

    def show_downloads():
        actions.key("cmd-alt-l")

    def show_extensions():
        actions.key("cmd-shift-x")


@mod.action_class
class Actions:
    def overview_tabs():
        "Toggle tab overview in Orion"
        actions.key("cmd-shift-\\")
