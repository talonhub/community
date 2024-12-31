import os

from talon import (
    Context,
    Module,
    actions,
    app,
    clip,
    cron,
    ctrl,
    imgui,
    ui,
    noise,
    registry,
    settings, 
    tap,
)

key = actions.key
self = actions.self
scroll_amount = 0
click_job = None
scroll_job = None
gaze_job = None
cancel_scroll_on_pop = True
control_mouse_forced = False

hiss_scroll_up = False

# Setting for how much percent of the screen you should gaze further from the reference point before scrolling starts.
scroll_offset = 0.12
# Setting for how fast scrolling should be depending on the distance from the reference point.
def scroll_formula(diff):
    return 10 + pow(10 * abs(diff), 3.5)


# Setting for the number of eye locations we should take the average from, increasing this will increase accuracy and increase latency.
eye_avg = 20

default_cursor = {
    "AppStarting": r"%SystemRoot%\Cursors\aero_working.ani",
    "Arrow": r"%SystemRoot%\Cursors\aero_arrow.cur",
    "Hand": r"%SystemRoot%\Cursors\aero_link.cur",
    "Help": r"%SystemRoot%\Cursors\aero_helpsel.cur",
    "No": r"%SystemRoot%\Cursors\aero_unavail.cur",
    "NWPen": r"%SystemRoot%\Cursors\aero_pen.cur",
    "Person": r"%SystemRoot%\Cursors\aero_person.cur",
    "Pin": r"%SystemRoot%\Cursors\aero_pin.cur",
    "SizeAll": r"%SystemRoot%\Cursors\aero_move.cur",
    "SizeNESW": r"%SystemRoot%\Cursors\aero_nesw.cur",
    "SizeNS": r"%SystemRoot%\Cursors\aero_ns.cur",
    "SizeNWSE": r"%SystemRoot%\Cursors\aero_nwse.cur",
    "SizeWE": r"%SystemRoot%\Cursors\aero_ew.cur",
    "UpArrow": r"%SystemRoot%\Cursors\aero_up.cur",
    "Wait": r"%SystemRoot%\Cursors\aero_busy.ani",
    "Crosshair": "",
    "IBeam": "",
}

# todo figure out why notepad++ still shows the cursor sometimes.
hidden_cursor = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), r"Resources\HiddenCursor.cur"
)

mod = Module()
ctx_global = Context()
ctx_zoom_triggered = Context()
ctx_control_mouse_enabled = Context()
ctx_is_dragging = Context()

mod.list(
    "mouse_button", desc="List of mouse button words to mouse_click index parameter"
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
    "mouse_enable_hiss_scroll",
    type=bool,
    default=False,
    desc="Hiss noise scrolls down when enabled",
)
mod.setting(
    "mouse_wake_hides_cursor",
    type=bool,
    default=False,
    desc="When enabled, mouse wake will hide the cursor. mouse_wake enables zoom mouse.",
)
mod.setting(
    "mouse_hide_mouse_gui",
    type=bool,
    default=False,
    desc="When enabled, the 'Scroll Mouse' GUI will not be shown.",
)
mod.setting(
    "mouse_continuous_scroll_amount",
    type=int,
    default=80,
    desc="The default amount used when scrolling continuously",
)
mod.setting(
    "mouse_wheel_down_amount",
    type=int,
    default=120,
    desc="The amount to scroll up/down (equivalent to mouse wheel on Windows by default)",
)
mod.setting(
    "mouse_wheel_horizontal_amount",
    type=int,
    default=40,
    desc="The amount to scroll left/right",
)
mod.setting(
    "mouse_drag_use_control_mouse",
    type=bool,
    default=False,
    desc="Boolean that specifies whether or not to use control mouse for dragging",
)

continuous_scoll_mode = None


@imgui.open(x=700, y=0)
def gui_wheel(gui: imgui.GUI):
    gui.text(f"Scroll mode: {continuous_scoll_mode}")
    gui.line()
    if gui.button("Wheel Stop [stop scrolling]"):
        actions.user.mouse_scroll_stop()


@ctx_global.action_class("tracking")
class TrackingActions:
    # other tab functions should already be implemented in
    # code/platforms/mac/app.py
    def zoom():
        ctx_zoom_triggered.tags = ["user.zoom_mouse_activated"]
        actions.next()

    def zoom_cancel():
        actions.next()

    def control_zoom_toggle(state: bool = None) -> None:    
        actions.next()

        if state:
            ctx_control_mouse_enabled.tags = ["user.zoom_mouse_enabled"]
        else:
            ctx_control_mouse_enabled.tags = []


@mod.action_class
class Actions:
    def zoom_clear_activated():
        """"""
        ctx_zoom_triggered.tags = []

    def zoom_close():
        """Closes an in-progress zoom. Talon will move the cursor position but not click."""
        actions.tracking.zoom_cancel()

    def mouse_show_cursor():
        """Shows the cursor"""
        show_cursor_helper(True)

    def mouse_hide_cursor():
        """Hides the cursor"""
        show_cursor_helper(False)

    def mouse_wake():
        """Enable control mouse, zoom mouse, and disables cursor"""
        if actions.tracking.control_enabled():            
            actions.tracking.control_toggle(False)
            actions.tracking.control1_toggle(False)
            ctx_control_mouse_enabled.tags = []
            ctx_is_dragging.tags = []
        try:
            # actions.user.clickless_mouse_enable()
            actions.tracking.control_zoom_toggle(True)
            ctx_is_dragging.tags = []

        except Exception as e:
            print(e)
            actions.app.notify(e)
            actions.sleep("500ms")
            # actions.user.talon_restart()

        if settings.get("user.mouse_wake_hides_cursor") >= 1:
            show_cursor_helper(False)

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


    def mouse_drag_end():
        """Releases any held mouse buttons"""
        
        global control_mouse_forced
        buttons_held_down = list(ctrl.mouse_buttons_down())
        for button in buttons_held_down:
            ctrl.mouse_click(button=button, up=True)

        ctx_is_dragging.tags = []
        
        if settings.get("user.mouse_drag_use_control_mouse"):
            if control_mouse_forced:
                actions.user.mouse_toggle_control_mouse()

                control_mouse_forced = False

                # reenable zoom mouse
                if not actions.tracking.control_zoom_enabled():
                    # print("attempting to re enable zoom mouse")
                    actions.user.mouse_toggle_zoom_mouse()

    def mouse_is_dragging():
        """Returns whether or not a drag is in progress"""
        buttons_held_down = list(ctrl.mouse_buttons_down())
        return len(buttons_held_down) > 0

    def mouse_sleep():
        """Disables control mouse, zoom mouse, and re-enables cursor"""
        global control_mouse_forced
        actions.tracking.control_zoom_toggle(False)
        actions.tracking.control_toggle(False)
        actions.tracking.control1_toggle(False)
        actions.user.clickless_mouse_disable()

        show_cursor_helper(True)
        stop_scroll()

        # todo: fixme temporary fix for drag command
        button_down = len(list(ctrl.mouse_buttons_down())) > 0
        if button_down:
            ctrl.mouse_click(button=0, up=True)
        ctx_control_mouse_enabled.tags = []
        ctx_is_dragging.tags = [] 
        control_mouse_forced = False

    def mouse_scroll_down(amount: float = 1):
        """Scrolls down"""
        mouse_scroll(amount * settings.get("user.mouse_wheel_down_amount"))()

    def mouse_scroll_down_continuous():
        """Scrolls down continuously"""
        global continuous_scoll_mode
        continuous_scoll_mode = "scroll down continuous"
        mouse_scroll(settings.get("user.mouse_continuous_scroll_amount"))()

        if scroll_job is None:
            start_scroll()

        if settings.get("user.mouse_hide_mouse_gui") == 0:
            gui_wheel.show()

    def mouse_scroll_up(amount: float = 1):
        """Scrolls up"""
        mouse_scroll(-amount * settings.get("user.mouse_wheel_down_amount"))()

    def mouse_scroll_up_continuous():
        """Scrolls up continuously"""
        global continuous_scoll_mode
        continuous_scoll_mode = "scroll up continuous"
        mouse_scroll(-settings.get("user.mouse_continuous_scroll_amount"))()

        if scroll_job is None:
            start_scroll()
        if settings.get("user.mouse_hide_mouse_gui") == 0:
            gui_wheel.show()

    def mouse_scroll_left(amount: float = 1):
        """Scrolls left"""
        actions.mouse_scroll(0, -amount * settings.get("user.mouse_wheel_horizontal_amount"))

    def mouse_scroll_right(amount: float = 1):
        """Scrolls right"""
        actions.mouse_scroll(0, amount * settings.get("user.mouse_wheel_horizontal_amount"))

    def mouse_scroll_stop():
        """Stops scrolling"""
        stop_scroll()
    
    def mouse_is_continuous_scrolling():
        """Returns whether a continuous_scoll_mode is enabled"""
        if continuous_scoll_mode:
            return True
        

    def mouse_gaze_scroll():
        """Starts gaze scroll"""
        global continuous_scoll_mode
        continuous_scoll_mode = "gaze scroll"

        start_cursor_scrolling()
        if settings.get("user.mouse_hide_mouse_gui") == 0:
            gui_wheel.show()

        # enable 'control mouse' if eye tracker is present and not enabled already
        global control_mouse_forced
        if not actions.tracking.control_enabled():
            actions.tracking.control_toggle(True)
            control_mouse_forced = True

    def mouse_gaze_scroll_cursor():
        # Scroll the window if your eyes gaze up or down relative to the current curser position
        """Starts gaze scroll cursor"""
        global continuous_scoll_mode
        continuous_scoll_mode = "gaze scroll"

        start_cursor_scrolling()
        if settings.get("user.mouse_hide_mouse_gui") == 0:
            gui_wheel.show()

    def copy_mouse_position():
        """Copy the current mouse position coordinates"""
        position = ctrl.mouse_pos()
        clip.set_text(repr(position))

    def mouse_move_center_active_window():
        """move the mouse cursor to the center of the currently active window"""
        rect = ui.active_window().rect
        ctrl.mouse_move(rect.left + (rect.width / 2), rect.top + (rect.height / 2))
        
    def mouse_toggle_zoom_mouse():
        """Toggles the zoom mouse"""
        actions.tracking.control_zoom_toggle()
        
        if actions.tracking.control_enabled():                      
            actions.tracking.control_toggle(False)
            actions.tracking.control1_toggle(False)

        # if actions.tracking.control_zoom_enabled():
        #     actions.user.clickless_mouse_enable()

    def mouse_toggle_control_mouse():
        """Toggles the control mouse"""
        actions.tracking.control_toggle()
        if actions.tracking.control_enabled():            
            if actions.tracking.control_zoom_enabled():
                actions.tracking.control_zoom_toggle()
            actions.user.clickless_mouse_disable()


    def hiss_scroll_up():
        """Change mouse hiss scroll direction to up"""
        global hiss_scroll_up
        hiss_scroll_up = True

    def hiss_scroll_down():
        """Change mouse hiss scroll direction to down"""
        global hiss_scroll_up
        hiss_scroll_up = False



def show_cursor_helper(show):
    """Show/hide the cursor"""
    if app.platform == "windows":
        import ctypes
        import winreg

        import win32con

        try:
            Registrykey = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors", 0, winreg.KEY_WRITE
            )

            for value_name, value in default_cursor.items():
                if show:
                    winreg.SetValueEx(
                        Registrykey, value_name, 0, winreg.REG_EXPAND_SZ, value
                    )
                else:
                    winreg.SetValueEx(
                        Registrykey, value_name, 0, winreg.REG_EXPAND_SZ, hidden_cursor
                    )

            winreg.CloseKey(Registrykey)

            ctypes.windll.user32.SystemParametersInfoA(
                win32con.SPI_SETCURSORS, 0, None, 0
            )

        except OSError:
            print(f"Unable to show_cursor({str(show)})")
    else:
        ctrl.cursor_visible(show)


def mouse_scroll(amount):
    def scroll():
        global scroll_amount
        if continuous_scoll_mode:
            if (scroll_amount >= 0) == (amount >= 0):
                scroll_amount += amount
            else:
                scroll_amount = amount
        actions.mouse_scroll(y=int(amount))

    return scroll


def scroll_continuous_helper():
    global scroll_amount
    # print("scroll_continuous_helper")
    if scroll_amount:
        actions.mouse_scroll(by_lines=False, y=int(scroll_amount / 10))


def start_scroll():
    global scroll_job
    scroll_job = cron.interval("60ms", scroll_continuous_helper)


def gaze_scroll():
    # print("gaze_scroll")
    x, y = ctrl.mouse_pos()

    # the rect for the window containing the mouse
    rect = None

    # on windows, check the active_window first since ui.windows() is not z-ordered
    if app.platform == "windows" and ui.active_window().rect.contains(x, y):
        rect = ui.active_window().rect
    else:
        windows = ui.windows()
        for w in windows:
            if w.rect.contains(x, y):
                rect = w.rect
                break

    if rect is None:
        # print("no window found!")
        return

    midpoint = rect.y + rect.height / 2
    amount = int(((y - midpoint) / (rect.height / 10)) ** 3)
    actions.mouse_scroll(by_lines=False, y=amount)

    # print(f"gaze_scroll: {midpoint} {rect.height} {amount}")


def gaze_scroll_cursor():
    # Scroll the window if your eyes gaze up or down relative to the current window position

    gaze_y = 0
    hist = mouse.eye_hist[-eye_avg:]
    for l, r in hist:
        gaze_y += l.gaze.y + r.gaze.y
    gaze_y /= 2 * len(hist)

    cursor_x, cursor_y = ctrl.mouse_pos()
    cursor_y /= main_screen.height
    diff_y = gaze_y - cursor_y

    if abs(diff_y) > scroll_offset:
        amount = int(scroll_formula(diff_y))
        if diff_y < 0 and amount > 0:
            amount = -amount
        actions.mouse_scroll(by_lines=False, y=amount)

def stop_scroll():
    global scroll_amount, scroll_job, gaze_job, continuous_scoll_mode
    scroll_amount = 0
    if scroll_job:
        cron.cancel(scroll_job)

    if gaze_job:
        cron.cancel(gaze_job)

    global control_mouse_forced
    if control_mouse_forced:
        actions.tracking.control_toggle(False)
        control_mouse_forced = False

    scroll_job = None
    gaze_job = None
    gui_wheel.hide()

    continuous_scoll_mode = None


def start_cursor_scrolling():
    global scroll_job, gaze_job
    stop_scroll()
    gaze_job = cron.interval("60ms", gaze_scroll)


@ctx_control_mouse_enabled.action_class("user")
class UserActions:
    def noise_trigger_pop():
        if settings.get("user.mouse_enable_pop_stops_scroll") >= 1 and (
            gaze_job or scroll_job
        ):
            # Allow pop to stop scroll
            stop_scroll()
        else:
            if actions.user.mouse_is_dragging(): 
                actions.user.mouse_drag_end()
            else:
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

    def noise_trigger_hiss(active: bool):
        if settings.get("user.mouse_enable_hiss_scroll"):
            if active:
                if hiss_scroll_up:
                    actions.user.mouse_scroll_up_continuous()
                else:
                    actions.user.mouse_scroll_down_continuous()
            else:
                actions.user.mouse_scroll_stop()            
     
