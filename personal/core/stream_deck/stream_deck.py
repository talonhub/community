from talon import ui, Module, Context, registry, actions, imgui, cron, app, scope
mod = Module()
ctx_zoom_mouse_enabled = Context()
ctx_zoom_mouse_enabled.matches = r"""
not user.running: Optikey Mouse
tag: user.zoom_mouse_enabled
and not tag: user.zoom_mouse_activated
and not tag: user.continuous_scrolling
"""


ctx_zoom_mouse_triggered = Context()
ctx_zoom_mouse_triggered.matches = r"""
tag: user.zoom_mouse_enabled
and tag: user.zoom_mouse_activated
and not tag: user.control_mouse_enabled
and not tag: user.continuous_scrolling
#and not tag: talon_plugins.eye_zoom_mouse.zoom_mouse_pedal
"""

ctx_control_mouse_enabled = Context()
ctx_control_mouse_enabled.matches  = r"""
tag: user.control_mouse_enabled
and not tag: user.continuous_scrolling
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

deck_cached_paths: dict = {}

@mod.action_class
class Actions:
    def deck_cache_path(serial: str):
        """Set deck cache"""
        global deck_cached_paths
        deck_cached_paths[serial] = actions.deck.current_path(serial)

    def deck_set_cached_path_and_clear(serial: str):
        """Set and clear deck cache"""
        global deck_cached_paths

        cache_path = deck_cached_paths.pop(serial, None)
        if cache_path:
            print(f"deck_set_cached_path_and_clear - returning deck {serial} to {cache_path}")
            actions.deck.goto(serial, cache_path)

    def deck_pedal_left():
        """left pedal"""
        actions.user.system_switcher()

    def deck_pedal_middle():
        """middle pedal"""
        if actions.tracking.control_zoom_enabled():
            actions.tracking.zoom()
            actions.deck.goto("A00SA3232MA4OZ", "zoom")

    def deck_pedal_right():
        """right pedal"""
        # trigger_home_row()
        actions.user.quick_pick_show()

    def deck1():
        """document string goes here"""
        if not actions.tracking.control_zoom_enabled():
            actions.tracking.control_zoom_toggle(True)

        actions.user.zoom_set_allowed(True)
        actions.tracking.zoom()
        actions.deck.goto("A00SA3232MA4OZ", "zoom")

    def deck2():
        """document string goes here"""

        trigger_home_row()
        

    def deck3():
        """document string goes here"""
        
        actions.user.mouse_scroll_down_continuous()
        actions.deck.goto("A00SA3232MA4OZ", "scrolling")


    def deck4():
        """document string goes here"""
        actions.user.mouse_scroll_up_continuous()
        actions.deck.goto("A00SA3232MA4OZ", "scrolling")


    def deck5():
        """document string goes here"""
        if actions.user.mouse_is_continuous_scrolling():
            actions.user.mouse_scroll_stop()


    def deck6():
        """document"""
        actions.user.move_cursor_to_gaze_point()


    def deck7():
        """document string goes here"""
        actions.user.quick_pick_show()
    
    def deck8():
        """document string goes here"""
        actions.user.system_switcher()

    def deck9():
        """document string goes here"""
        if actions.user.mouse_is_continuous_scrolling():
            actions.user.mouse_scroll_stop()
        else:
            actions.edit.undo()

    def deck10():
        """document string goes here"""
        actions.core.repeat_command(1)

    def deck11():
        """document string goes here"""
        actions.user.dictation_or_command_toggle()
    
    def deck12():
        """document string goes here"""
        # actions.user.dictation_or_command_toggle()
        actions.user.mouse_toggle_zoom_mouse()
    
    def deck13():
        """document string goes here"""
        actions.user.microphone_toggle()    
        
    def deck14():
        """document string goes here"""
        actions.user.microphone_toggle()
        # This shortcut for muting video conferencing applications only functions on windows 11
        # It is also not supported by new teams at the moment 
        actions.user.microphone_toggle_video_conference()
    
    def deck15():
        """document string goes here"""
        sleep_or_wake()

def on_ready():
    actions.deck.goto("A00SA3232MA4OZ", "default")

app.register("ready", on_ready)

        
        
        