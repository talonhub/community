from talon import Context, Module, actions, ctrl, settings, ui

ctx_global = Context()
ctx_zoom_triggered = Context()
ctx_control_mouse_enabled = Context()

mod = Module()

@mod.action_class
class Actions:
    def zoom_clear_activated():
        """"""
        ctx_zoom_triggered.tags = []
        actions.tracking.control_zoom_toggle(False)   

@ctx_control_mouse_enabled.action_class("user")
class UserActions:
    def noise_trigger_pop():
        dont_click = False

        # Allow pop to stop drag
        if settings.get("user.mouse_enable_pop_stops_drag"):
            if actions.user.mouse_drag_end():
                dont_click = True

        # Allow pop to stop scroll
        if settings.get("user.mouse_enable_pop_stops_scroll"):
            if actions.user.mouse_scroll_stop():
                dont_click = True

        if dont_click:
            return

        # Otherwise respect the mouse_enable_pop_click setting
        setting_val = settings.get("user.mouse_enable_pop_click")

        is_using_eye_tracker = (
            actions.tracking.control_zoom_enabled()
            or actions.tracking.control_enabled()
            or actions.tracking.control1_enabled()
        )

        should_click = (
            setting_val == 2 and not actions.tracking.control_zoom_enabled()
        ) or (
            setting_val == 1
            and is_using_eye_tracker
            and not actions.tracking.control_zoom_enabled()
        )

        if should_click:
            ctrl.mouse_click(button=0, hold=16000)         

@ctx_global.action_class("tracking")
class TrackingActions:
    def zoom():
        if not actions.user.mouse_is_continuous_scrolling() and actions.user.zoom_allowed():
            if actions.tracking.control_zoom_enabled():
                ctx_zoom_triggered.tags = ["user.zoom_mouse_activated"]
                actions.next()
                actions.deck.goto("A00SA3232MA4OZ", "zoom")

            else:
                ctx_zoom_triggered.tags = []
                actions.user.zoom_set_allowed(False)

    def zoom_cancel():
        if actions.tracking.control_zoom_enabled() or "user.zoom_mouse_activated" in ctx_zoom_triggered.tags:
            actions.user.zoom_set_allowed(False)
            actions.next()
            
    def control_zoom_toggle(state: bool = None) -> None:    
        actions.next(state)
        actions.user.zoom_set_allowed(False)

        if state:
            ctx_control_mouse_enabled.tags = ["user.zoom_mouse_enabled"]
        else:
            ctx_control_mouse_enabled.tags = []