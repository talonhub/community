import time
from typing import Literal

from talon import Context, Module, actions, app, cron, ctrl, imgui, settings, ui

continuous_scroll_mode = ""
scroll_job = None
gaze_job = None
scroll_dir: Literal[-1, 1] = 1
scroll_start_ts: float = 0
hiss_scroll_up = False
control_mouse_forced = False

mod = Module()
ctx = Context()


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
    "mouse_continuous_scroll_amount",
    type=int,
    default=8,
    desc="The default amount used when scrolling continuously",
)
mod.setting(
    "mouse_continuous_scroll_acceleration",
    type=float,
    default=1,
    desc="The maximum (linear) acceleration factor when scrolling continuously. 1=constant speed/no acceleration",
)
mod.setting(
    "mouse_enable_hiss_scroll",
    type=bool,
    default=False,
    desc="Hiss noise scrolls down when enabled",
)
mod.setting(
    "mouse_hide_mouse_gui",
    type=bool,
    default=False,
    desc="When enabled, the 'Scroll Mouse' GUI will not be shown.",
)


@imgui.open(x=700, y=0)
def gui_wheel(gui: imgui.GUI):
    gui.text(f"Scroll mode: {continuous_scroll_mode}")
    gui.line()
    if gui.button("Wheel Stop [stop scrolling]"):
        actions.user.mouse_scroll_stop()


@mod.action_class
class Actions:
    def mouse_scroll_up(amount: float = 1):
        """Scrolls up"""
        y = amount * settings.get("user.mouse_wheel_down_amount")
        actions.mouse_scroll(-y)

    def mouse_scroll_down(amount: float = 1):
        """Scrolls down"""
        y = amount * settings.get("user.mouse_wheel_down_amount")
        actions.mouse_scroll(y)

    def mouse_scroll_left(amount: float = 1):
        """Scrolls left"""
        x = amount * settings.get("user.mouse_wheel_horizontal_amount")
        actions.mouse_scroll(0, -x)

    def mouse_scroll_right(amount: float = 1):
        """Scrolls right"""
        x = amount * settings.get("user.mouse_wheel_horizontal_amount")
        actions.mouse_scroll(0, x)

    def mouse_scroll_up_continuous():
        """Scrolls up continuously"""
        mouse_scroll_continuous(-1)

    def mouse_scroll_down_continuous():
        """Scrolls down continuously"""
        mouse_scroll_continuous(1)

    def mouse_gaze_scroll():
        """Starts gaze scroll"""
        global gaze_job, continuous_scroll_mode, control_mouse_forced

        continuous_scroll_mode = "gaze scroll"
        gaze_job = cron.interval("16ms", scroll_gaze_helper)

        if not settings.get("user.mouse_hide_mouse_gui"):
            gui_wheel.show()

        # enable 'control mouse' if eye tracker is present and not enabled already
        if not actions.tracking.control_enabled():
            actions.tracking.control_toggle(True)
            control_mouse_forced = True

    def mouse_gaze_scroll_toggle():
        """If not scrolling, start gaze scroll, else stop scrolling."""
        if continuous_scroll_mode == "":
            actions.user.mouse_gaze_scroll()
        else:
            actions.user.mouse_scroll_stop()

    def mouse_scroll_stop() -> bool:
        """Stops scrolling"""
        global scroll_job, gaze_job, continuous_scroll_mode, control_mouse_forced

        continuous_scroll_mode = ""
        return_value = False

        if scroll_job:
            cron.cancel(scroll_job)
            scroll_job = None
            return_value = True

        if gaze_job:
            cron.cancel(gaze_job)
            gaze_job = None
            return_value = True

        if control_mouse_forced:
            actions.tracking.control_toggle(False)
            control_mouse_forced = False

        gui_wheel.hide()

        return return_value

    def hiss_scroll_up():
        """Change mouse hiss scroll direction to up"""
        global hiss_scroll_up
        hiss_scroll_up = True

    def hiss_scroll_down():
        """Change mouse hiss scroll direction to down"""
        global hiss_scroll_up
        hiss_scroll_up = False


@ctx.action_class("user")
class UserActions:
    def noise_trigger_hiss(active: bool):
        if settings.get("user.mouse_enable_hiss_scroll"):
            if active:
                if hiss_scroll_up:
                    actions.user.mouse_scroll_up_continuous()
                else:
                    actions.user.mouse_scroll_down_continuous()
            else:
                actions.user.mouse_scroll_stop()


def mouse_scroll_continuous(new_scroll_dir: Literal[-1, 1]):
    global scroll_job, scroll_dir, scroll_start_ts, continuous_scroll_mode

    if scroll_job:
        # Issuing a scroll in the same direction aborts scrolling
        if scroll_dir == new_scroll_dir:
            cron.cancel(scroll_job)
            scroll_job = None
            continuous_scroll_mode = ""
        # Issuing a scroll in the reverse direction resets acceleration
        else:
            scroll_dir = new_scroll_dir
            scroll_start_ts = time.perf_counter()
    else:
        scroll_dir = new_scroll_dir
        scroll_start_ts = time.perf_counter()
        continuous_scroll_mode = "scroll down continuous"
        scroll_continuous_helper()
        scroll_job = cron.interval("16ms", scroll_continuous_helper)

        if not settings.get("user.mouse_hide_mouse_gui"):
            gui_wheel.show()


def scroll_continuous_helper():
    scroll_amount = settings.get("user.mouse_continuous_scroll_amount")
    acceleration_setting = settings.get("user.mouse_continuous_scroll_acceleration")
    acceleration_speed = (
        1 + min((time.perf_counter() - scroll_start_ts) / 0.5, acceleration_setting - 1)
        if acceleration_setting > 1
        else 1
    )
    y = scroll_amount * acceleration_speed * scroll_dir
    actions.mouse_scroll(y)


def scroll_gaze_helper():
    x, y = ctrl.mouse_pos()

    # The window containing the mouse
    window = get_window_containing(x, y)

    if window is None:
        return

    rect = window.rect
    midpoint = rect.center.y
    amount = ((y - midpoint) / (rect.height / 10)) ** 3
    actions.mouse_scroll(amount)


def get_window_containing(x: float, y: float):
    # on windows, check the active_window first since ui.windows() is not z-ordered
    if app.platform == "windows" and ui.active_window().rect.contains(x, y):
        return ui.active_window()

    active = ui.active_window()

    found_active_window = False
    for window in ui.windows():
        if window == active:
            found_active_window = True
        if found_active_window and window.rect.contains(x, y):
            return window

    return None
