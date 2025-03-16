from talon import Context, Module, actions, ctrl, settings, ui

mod = Module()
ctx_global = Context()
ctx_zoom_triggered = Context()
ctx_control_mouse_enabled = Context()
ctx_is_dragging = Context()

mod.list(
    "mouse_button",
    desc="List of mouse button words to mouse_click index parameter",
)
mod.tag(
    "mouse_cursor_commands_enable", desc="Tag enables hide/show mouse cursor commands"
)
mod.tag(
    "control_mouse_enabled", desc="tag enabled when control mouse is enabled"
)
mod.tag(
    "zoom_mouse_enabled", desc="tag enabled when zoom mouse is enabled"
)
mod.tag(
    "zoom_mouse_activated", desc="tag enabled when zoom mouse is activated"
)
mod.tag(
    "mouse_is_dragging", desc="Tag indicates whether or not the mouse is currently being dragged"
)
mod.setting(
    "mouse_enable_pop_click",
    type=int,
    default=0,
    desc="Pop noise clicks left mouse button. 0 = off, 1 = on with eyetracker but not with zoom mouse mode, 2 = on but not with zoom mouse mode",
)
mod.setting(
    "mouse_enable_pop_stops_scroll",
    type=bool,
    default=False,
    desc="When enabled, pop stops continuous scroll modes (wheel upper/downer/gaze)",
)
mod.setting(
    "mouse_enable_pop_stops_drag",
    type=bool,
    default=False,
    desc="When enabled, pop stops mouse drag",
)
mod.setting(
    "mouse_wake_hides_cursor",
    type=bool,
    default=False,
    desc="When enabled, mouse wake will hide the cursor. mouse_wake enables zoom mouse.",
)
mod.setting(
    "mouse_drag_use_control_mouse",
    type=bool,
    default=False,
    desc="When enabled, drag will enable control mouse",
)


@mod.action_class
class Actions:
    def zoom_clear_activated():
        """"""
        ctx_zoom_triggered.tags = []
        actions.tracking.control_zoom_toggle(False)

    def mouse_wake():
        """Enable control mouse, zoom mouse, and disables cursor"""
        if actions.tracking.control_enabled():            
            actions.tracking.control_toggle(False)
            actions.tracking.control1_toggle(False)
            ctx_control_mouse_enabled.tags = []
            ctx_is_dragging.tags = []
        try:
            # actions.user.clickless_mouse_enable()
            # actions.tracking.control_zoom_toggle(True)
            ctx_is_dragging.tags = []

        except Exception as e:
            print(e)
            actions.app.notify(e)
            actions.sleep("500ms")
            # actions.user.talon_restart()

        if settings.get("user.mouse_wake_hides_cursor"):
            actions.user.mouse_cursor_hide()

    def mouse_drag(button: int):
        """Press and hold/release a specific mouse button for dragging"""
        # Clear any existing drags
        global control_mouse_forced
        if actions.user.mouse_is_dragging():
            actions.user.mouse_drag_end()
        else:
            # Start drag
            ctx_is_dragging.tags = ["user.mouse_is_dragging"]

            ctrl.mouse_click(button=button, down=True)

            if settings.get("user.mouse_drag_use_control_mouse"):
                if not actions.tracking.control_enabled():
                    # print("force enabling control mouse")
                    control_mouse_forced = True
                    actions.user.mouse_toggle_control_mouse()

    def mouse_drag_end() -> bool:
        """Releases any held mouse buttons"""
        
        global control_mouse_forced
        buttons = ctrl.mouse_buttons_down()
        drag_stopped = False
        if buttons:
            for button in buttons:
                actions.mouse_release(button)
            drag_stopped = True
			
        ctx_is_dragging.tags = []
        
        if settings.get("user.mouse_drag_use_control_mouse"):
            if control_mouse_forced:
                actions.user.mouse_toggle_control_mouse()

                control_mouse_forced = False

                # reenable zoom mouse
                if not actions.tracking.control_zoom_enabled():
                    # print("attempting to re enable zoom mouse")
                    actions.user.mouse_toggle_zoom_mouse()
        
        return drag_stopped

    def mouse_drag_toggle(button: int):
        """If the button is held down, release the button, else start dragging"""
        if button in ctrl.mouse_buttons_down():
            actions.mouse_release(button)
        else:
            actions.mouse_drag(button)

    def mouse_is_dragging():
        """Returns whether or not a drag is in progress"""
        buttons_held_down = list(ctrl.mouse_buttons_down())
        return len(buttons_held_down) > 0
		
    def mouse_sleep():
        """Disables control mouse, zoom mouse, and re-enables cursor"""
        actions.tracking.control_zoom_toggle(False)
        actions.tracking.control_toggle(False)
        actions.tracking.control1_toggle(False)
        actions.user.clickless_mouse_disable()

        actions.user.mouse_cursor_show()
        actions.user.mouse_scroll_stop()
        actions.user.mouse_drag_end()

    def copy_mouse_position():
        """Copy the current mouse position coordinates"""
        x, y = actions.mouse_x(), actions.mouse_y()
        actions.clip.set_text(f"{x}, {y}")

    def mouse_move_center_active_window():
        """Move the mouse cursor to the center of the currently active window"""
        rect = ui.active_window().rect
        actions.mouse_move(rect.center.x, rect.center.y)


    def mouse_toggle_control_mouse():
        """Toggles the control mouse"""
        actions.tracking.control_toggle()
        if actions.tracking.control_enabled():            
            if actions.tracking.control_zoom_enabled():
                actions.tracking.control_zoom_toggle()
            actions.user.clickless_mouse_disable()



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
            
ctx_global = Context()
@ctx_global.action_class("tracking")
class TrackingActions:
    def zoom():
        if not actions.user.mouse_is_continuous_scrolling():
            if actions.tracking.control_zoom_enabled():
                ctx_zoom_triggered.tags = ["user.zoom_mouse_activated"]
                actions.next()
            else:
                ctx_zoom_triggered.tags = []

    def zoom_cancel():
        if actions.tracking.control_zoom_enabled() or "user.zoom_mouse_activated" in ctx_zoom_triggered.tags:
            actions.next()
            
    def control_zoom_toggle(state: bool = None) -> None:    
        actions.next(state)

        if state:
            ctx_control_mouse_enabled.tags = ["user.zoom_mouse_enabled"]
        else:
            ctx_control_mouse_enabled.tags = []