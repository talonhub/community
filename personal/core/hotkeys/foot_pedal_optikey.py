from talon import ui, Module, Context, registry, actions, imgui, cron, track, app
from talon_plugins.eye_mouse import config, toggle_camera_overlay, toggle_control, mouse
import sys


# (3655, 202)
# (3616, 377)
# (3668, 618)
# (3673, 833)
# (3682, 959)

# (3647, 1628)


ctx_optikey_running = Context()
ctx_optikey_running.matches = r"""
os: windows
user.running: Optikey Mouse
"""


@ctx_optikey_running.action_class("user")
class Actions:
    def foot_pedal_left_left():
        """document string goes here"""
        actions.mouse_move(3655, 202)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def foot_pedal_left_middle():
        """document string goes here"""
        actions.mouse_move(3616, 377)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def foot_pedal_left_right():
        """document string goes here"""
        actions.mouse_move(3616, 618)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def foot_pedal_right_left():
        """document string goes here"""
        actions.mouse_move(3616, 833)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def foot_pedal_right_middle():
        """document string goes here"""
        actions.mouse_move(3616, 959)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def foot_pedal_right_right():
        """document string goes here"""
        actions.mouse_move(3616, 1628)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)


if app.platform == "windows":
    from pynput.mouse import Listener

    def on_move(x, y):
        print("Pointer moved to {0}".format((x, y)))

    def on_click(x, y, button, pressed):
        if config.control_mouse:
            toggle_control(False)

    def on_scroll(x, y, dx, dy):
        # print(str(e))
        if config.control_mouse:
            toggle_control(False)

    # def on_click(e):
    #     # print("on_click: " + str(e))
    #     if zoom_mouse.optikey_mouse:
    #         zoom_mouse.optikey_mouse = False
    #         toggle_control(False)
    #         if config.hide_cursor_for_control_mouse:
    #             actions.user.mouse_show_cursor()

    # def on_scroll(e):
    #     # print(str(e))
    #     if zoom_mouse.optikey_mouse:
    #         zoom_mouse.optikey_mouse = False
    #         toggle_control(False)
    #         if config.hide_cursor_for_control_mouse:
    #             actions.user.mouse_show_cursor()
    listener = Listener(on_click=on_click, on_scroll=on_scroll)
    listener.start()
