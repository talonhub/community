import contextlib
import time

from talon import actions, ctrl, ui, Context
ctx = Context()
ctx.matches = r"""
os: mac
"""

@contextlib.contextmanager
def _drag_window_mac(win=None):
    if win is None:
        win = ui.active_window()
    fs = win.children.find(AXSubrole="AXFullScreenButton")[0]
    rect = fs.AXFrame["$rect2d"]
    x = rect["x"] + rect["width"] + 5
    y = rect["y"] + rect["height"] / 2
    ctrl.mouse_move(x, y)
    ctrl.mouse_click(button=0, down=True)
    yield
    time.sleep(0.1)
    ctrl.mouse_click(button=0, up=True)

@ctx.action_class("user")
class MacActions:
    def desktop(number: int):
        if number < 10:
            actions.key("ctrl-{}".format(number))

    def desktop_next():
        actions.key("ctrl-right")

    def desktop_last():
        actions.key("ctrl-left")

    def desktop_show():
        actions.key("ctrl-up")

    def window_move_desktop_left():
        with _drag_window_mac():
            actions.key("ctrl-cmd-alt-left")

    def window_move_desktop_right():
        with _drag_window_mac():
            actions.key("ctrl-cmd-alt-right")

    def window_move_desktop(desktop_number: int):
        if ui.apps(bundle="com.amethyst.Amethyst"):
            actions.key(f"ctrl-alt-shift-{desktop_number}")
        else:
            with _drag_window_mac():
                actions.key(f"ctrl-{desktop_number}")
