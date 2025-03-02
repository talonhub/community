# defines the default app actions for linux

from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: linux
"""


@ctx.action_class("app")
class AppActions:
    # app.preferences()

    def tab_close():
        actions.key("ctrl-w")

    def tab_next():
        actions.key("ctrl-tab")

    def tab_open():
        actions.key("ctrl-t")

    def tab_previous():
        actions.key("ctrl-shift-tab")

    def tab_reopen():
        actions.key("ctrl-shift-t")

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
