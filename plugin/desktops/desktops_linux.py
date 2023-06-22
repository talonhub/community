from talon import Context, actions, ui

ctx = Context()
ctx.matches = r"""
os: linux
"""


@ctx.action_class("user")
class Actions:
    def desktop(number: int):
        ui.switch_workspace(number)

    def desktop_next():
        actions.user.desktop(ui.active_workspace() + 1)

    def desktop_last():
        actions.user.desktop(ui.active_workspace() - 1)

    def desktop_show():
        actions.key("super")

    def window_move_desktop(desktop_number: int):
        ui.active_window().workspace = desktop_number
        actions.user.desktop(desktop_number)

    def window_move_desktop_left():
        actions.user.window_move_desktop(ui.active_workspace() - 1)

    def window_move_desktop_right():
        actions.user.window_move_desktop(ui.active_workspace() + 1)
