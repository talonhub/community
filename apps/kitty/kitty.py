from talon import Context, actions

ctx = Context()
ctx.matches = r"""
app: kitty
os: linux
"""


@ctx.action_class("app")
class AppActions:
    def tab_open():
        actions.key("ctrl-shift-t")

    def tab_close():
        actions.key("ctrl-shift-q")

    def tab_next():
        actions.key("ctrl-shift-right")

    def tab_previous():
        actions.key("ctrl-shift-left")


@ctx.action_class("user")
class UserActions:
    def split_flip():
        actions.key("ctrl-shift-l")

    def split_window():
        actions.key("ctrl-shift-enter")

    def split_clear():
        actions.key("ctrl-shift-w")

    def split_next():
        actions.key("ctrl-shift-]")

    def split_last():
        actions.key("ctrl-shift-[")

    def split_window_right():
        actions.key("ctrl-shift-f")

    def split_window_left():
        actions.key("ctrl-shift-b")

    def split_number(index: int):
        actions.key("ctrl-shvift-{number}")
