from talon import ui, Module, Context, registry, actions, imgui, cron, track
import sys

mod = Module()


@mod.action_class
class Actions:
    def foot_pedal_left_left():
        """document string goes here"""
        actions.user.system_switcher()

    def foot_pedal_left_middle():
        """document string goes here"""
        actions.user.system_last_application()

    def foot_pedal_left_right():
        """document string goes here"""
        actions.user.system_search()

    def foot_pedal_right_left():
        """document string goes here"""
        actions.tracking.control_zoom_toggle()
        # actions.key("pageup")

    def foot_pedal_right_middle():
        """document string goes here"""
        actions.user.microphone_toggle()

    def foot_pedal_right_right():
        """document string goes here"""
        if not actions.speech.enabled():
            actions.speech.enable()
            actions.user.microphone_preferred()
            actions.user.mouse_wake()
            actions.user.hud_enable()
            # actions.user.clickless_mouse_enable()
        else:
            actions.user.sleep_all()
            actions.sound.set_microphone("None")
            actions.user.mouse_sleep()
            actions.user.hud_disable()
            # actions.user.clickless_mouse_disable()
