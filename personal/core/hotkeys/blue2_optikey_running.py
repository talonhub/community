from talon import ui, Module, Context, registry, actions, imgui, cron, track, app
from talon_plugins.eye_mouse import config, toggle_camera_overlay, toggle_control, mouse
import sys

mod = Module()
ctx_zoom_mouse_enabled_use_pedal = Context()
ctx_zoom_mouse_enabled_use_pedal.matches = r"""
user.running: Optikey Mouse
"""


@ctx_zoom_mouse_enabled_use_pedal.action_class("user")
class WindowsZoomMouseInactiveActions:
    def blue2_s1():
        """document string goes here"""
        actions.mouse_move(3655, 202)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def blue2_s2():
        """document string goes here"""
        actions.mouse_move(3616, 377)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def blue2_s3():
        """document string goes here"""
        actions.mouse_move(3616, 618)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def blue2_s4():
        """document string goes here"""
        # print('scroll up')
        actions.mouse_move(3616, 833)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def blue2_s5():
        """document string goes here"""
        # actions.user.system_task_view()
        actions.mouse_move(3616, 959)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def blue2_s6():
        """document"""
        actions.mouse_move(3616, 1628)
        actions.sleep("100ms")
        actions.key("f22")
        toggle_control(True)

    def blue2_s7():
        """document string goes here"""
        actions.tracking.control_zoom_toggle()

    def blue2_s8():
        """document string goes here"""
        actions.user.microphone_toggle()
