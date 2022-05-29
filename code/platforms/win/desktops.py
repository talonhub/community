from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: windows
"""


@ctx.action_class("user")
class Actions:
    # def desktop(number: int):

    def desktop_next():
        actions.key("super-ctrl-right")

    def desktop_last():
        actions.key("super-ctrl-left")

    def desktop_show():
        actions.key("super-tab")

    # def window_move_desktop_left():

    # def window_move_desktop_right():

    # def window_move_desktop(desktop_number: int):
