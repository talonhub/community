# defines the default app actions for linux

from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: linux
"""


@ctx.action_class("app")
class AppActions:
    # app.preferences()

    def window_close():
        actions.key("alt-f4")

    def window_hide():
        actions.key("alt-space n")

    def window_hide_others():
        actions.key("win-d alt-tab")

    def window_open():
        actions.key("ctrl-n")


@ctx.action_class("user")
class UserActions:
    def switcher_focus_last():
        actions.key("alt-tab")
