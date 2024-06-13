from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
"""


@ctx.action_class("app")
class AppActions:
    def tab_close():
        actions.key("cmd-w")

    def tab_next():
        actions.key("ctrl-tab")

    def tab_open():
        actions.key("cmd-t")

    def tab_previous():
        actions.key("ctrl-shift-tab")

    def tab_reopen():
        actions.key("cmd-shift-t")
