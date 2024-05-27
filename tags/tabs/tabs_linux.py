from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: linux
"""


@ctx.action_class("app")
class AppActions:
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
