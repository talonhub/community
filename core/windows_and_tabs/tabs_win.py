from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: windows
"""


@ctx.action_class("user")
class UserActions:
    def tab_move_left():
        actions.key("ctrl-shift-pageup")

    def tab_move_right():
        actions.key("ctrl-shift-pagedown")
