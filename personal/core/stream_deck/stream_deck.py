from talon import ui, Module, Context, registry, actions, imgui, cron, app, scope
mod = Module()
ctx_zoom_mouse_enabled = Context()
ctx_zoom_mouse_enabled.matches = r"""
not user.running: Optikey Mouse
tag: talon_plugins.eye_zoom_mouse.zoom_mouse_enabled
and not tag: talon_plugins.eye_zoom_mouse.zoom_mouse_activated
"""


ctx_zoom_mouse_triggered = Context()
ctx_zoom_mouse_triggered.matches = r"""
tag: talon_plugins.eye_zoom_mouse.zoom_mouse_enabled
and tag: talon_plugins.eye_zoom_mouse.zoom_mouse_activated
and not tag: user.control_mouse_enabled
#and not tag: talon_plugins.eye_zoom_mouse.zoom_mouse_pedal
"""

ctx_control_mouse_enabled = Context()
ctx_control_mouse_enabled.matches  = r"""
tag: user.control_mouse_enabled
"""
def sleep_or_wake():
    if not actions.speech.enabled():
        actions.speech.enable()
        actions.user.microphone_preferred()
        actions.user.mouse_wake()
        # todo: remove when the talon_hud perf is fixed on rust branch
        if "user.talon_hud_available" in scope.get("tag"):
            actions.user.hud_enable()
        actions.user.connect_ocr_eye_tracker()
        # actions.user.clickless_mouse_enable()
    else:
        actions.user.sleep_all()
        actions.sound.set_microphone("None")
        actions.user.mouse_sleep()
        # todo: remove when the talon_hud perf is fixed on rust branch
        if "user.talon_hud_available" in scope.get("tag"):
            actions.user.hud_disable()

        actions.user.disconnect_ocr_eye_tracker()
        actions.user.disconnect_ocr_eye_tracker()
        actions.user.hide_gaze_ocr_options()
        # actions.user.clickless_mouse_disable()


def trigger_home_row():
    if app.platform == "mac":
        # actions.key("cmd-shift-space")
        if "user.homerow_search" not in registry.tags:
            actions.user.homerow_search("")
        else:
            actions.key("escape")
    elif app.platform == "windows":
        actions.key("ctrl-m")


@mod.action_class
class Actions:
    def deck_pedal_left():
        """left pedal"""
        actions.user.system_switcher()

    def deck_pedal_middle():
        """middle pedal"""
        actions.talon_plugins.eye_zoom_mouse.mouse_trigger()

    def deck_pedal_right():
        """right pedal"""
        trigger_home_row()

    def deck1():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_trigger()


    def deck2():
        """document string goes here"""

        trigger_home_row()
        

    def deck3():
        """document string goes here"""
        
        actions.user.system_switcher()


    def deck4():
        """document string goes here"""
        
        actions.edit.undo()


    def deck5():
        """document string goes here"""
        
        actions.core.repeat_command(1)


    def deck6():
        """document"""
        actions.user.move_cursor_to_gaze_point()


    def deck7():
        """document string goes here"""
        actions.user.quick_pick_show()
        

    def deck8():
        """document string goes here"""
        actions.user.mouse_scroll_down_continuous()

    def deck9():
        """document string goes here"""
        actions.user.mouse_scroll_up_continuous()

    def deck10():
        """document string goes here"""
        actions.user.mouse_scroll_stop()

    def deck11():
        """document string goes here"""
        actions.user.move_cursor_to_gaze_point()
    
    def deck12():
        """document string goes here"""
        actions.user.mouse_toggle_zoom_mouse()
    
    def deck13():
        """document string goes here"""
        actions.user.dictation_or_command_toggle()
    
    def deck14():
        """document string goes here"""
        actions.user.microphone_toggle()
    
    def deck15():
        """document string goes here"""
        sleep_or_wake()
    
@ctx_zoom_mouse_triggered.action_class("user")
class WindowsZoomMouseTriggerActions:
    def deck_pedal_left():
        """left pedal"""
        actions.talon_plugins.eye_zoom_mouse.double_click()

    def deck_pedal_middle():
        """middle pedal"""
        actions.talon_plugins.eye_zoom_mouse.mouse_trigger()

    def deck_pedal_right():
        """right pedal"""
        actions.talon_plugins.eye_zoom_mouse.right_click()

    def deck1():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_trigger()

    def deck2():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.right_click()

    def deck3():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.double_click()

    def deck4():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.triple_click()

    def deck5():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_drag()

    def deck6():
        """document"""
        actions.talon_plugins.eye_zoom_mouse.mouse_move()

@ctx_control_mouse_enabled.action_class("user")
class ControlMouseEnabled:
    def deck_pedal_left():
        """left pedal"""
        actions.mouse_click(0)
        actions.mouse_click(0)

    def deck_pedal_middle():
        """middle pedal"""
        actions.mouse_click(0)

    def deck_pedal_right():
        """right pedal"""
        actions.mouse_click(1)
    def deck1():
        """document string goes here"""
        actions.mouse_click(0)

    def deck2():
        """document string goes here"""
        actions.mouse_click(1)
        

    def deck3():
        """document string goes here"""
        actions.mouse_click(0)
        actions.mouse_click(0)

    def deck4():
        """document string goes here"""
        actions.mouse_click(0)
        actions.mouse_click(0)
        actions.mouse_click(0)
        

    def deck5():
        """document string goes here"""
        actions.user.mouse_drag(0)
        actions.user.grid_close()
        

    def deck6():
        """document string goes here"""
        actions.mouse_move()

    def pedal_left_left():
        actions.mouse_click(0)
        actions.mouse_click(0)

    def pedal_left_right():
        actions.mouse_click(1)
     
    def pedal_left_middle():
        actions.mouse_click(0)
        
        
        