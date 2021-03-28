from talon import ctrl, ui, Module, Context, actions, clip, app
from talon.experimental.locate import locate_hover

ctx = Context()
mod = Module()

mod.apps.chrome = "app.name: Google Chrome"
mod.apps.chrome = "app.name: chrome.exe"

ctx.matches = r"""
app: chrome
"""


@ctx.action_class("user")
class user_actions:
    def tab_jump(number: int):
        if number < 9:
            if app.platform == "mac":
                actions.key("cmd-{}".format(number))
            else:
                actions.key("ctrl-{}".format(number))

    def tab_final():
        if app.platform == "mac":
            actions.key("cmd-9")
        else:
            actions.key("ctrl-9")


@mod.action_class
class Actions:
    def fill_password():
        """Move mouse to last pass fill password button"""
        locate_hover("templates/fill-password.png")