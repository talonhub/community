import contextlib
import time

from talon import Context, actions, ctrl, ui

ctx = Context()
ctx.matches = r"""
os: mac
"""


@contextlib.contextmanager
def _drag_window_mac(win=None):
    if win is None:
        win = ui.active_window()
    fs = win.children.find(AXSubrole="AXFullScreenButton")[0]
    rect = fs.AXFrame
    x = rect.x + rect.width + 5
    y = rect.y + rect.height / 2
    previous_position = ctrl.mouse_pos()
    ctrl.mouse_move(x, y)
    ctrl.mouse_click(button=0, down=True)
    yield
    time.sleep(0.1)
    ctrl.mouse_click(button=0, up=True)
    ctrl.mouse_move(*previous_position)


@ctx.action_class("user")
class MacActions:
    def desktop(number: int):
        if number < 10:
            actions.key(f"ctrl-{number}")

    def desktop_next():
        actions.key("ctrl-right")

    def desktop_last():
        actions.key("ctrl-left")

    def desktop_show():
        actions.key("ctrl-up")

    def window_move_desktop_left():
        with _drag_window_mac():
            actions.user.desktop_last()

    def window_move_desktop_right():
        with _drag_window_mac():
            actions.user.desktop_next()

    def window_move_desktop(desktop_number: int):
        # TODO: amethyst stuff should be pulled out into a separate file
        if ui.apps(bundle="com.amethyst.Amethyst"):
            actions.key(f"ctrl-alt-shift-{desktop_number}")
        else:
            with _drag_window_mac():
                actions.user.desktop(desktop_number)
