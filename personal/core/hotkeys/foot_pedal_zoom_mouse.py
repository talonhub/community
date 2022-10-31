from talon import ui, Module, Context, registry, actions, imgui, cron, track
import sys

ctx_zoom_mouse_triggered = Context()
ctx_zoom_mouse_triggered.matches = r"""
tag: talon_plugins.eye_zoom_mouse.zoom_mouse_enabled
and tag: talon_plugins.eye_zoom_mouse.zoom_mouse_activated
"""


@ctx_zoom_mouse_triggered.action_class("user")
class WindowsZoomMouseActiveActions:
    def foot_pedal_left_left():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_trigger()

    def foot_pedal_left_middle():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.right_click()

    def foot_pedal_left_right():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.double_click()

    def foot_pedal_right_left():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.triple_click()

    def foot_pedal_right_middle():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_drag()

    def foot_pedal_right_right():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_move()
