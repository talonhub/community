import time
from typing import Literal, Optional

from talon import Context, Module, actions, app, cron, ctrl, imgui, settings, ui

continuous_scroll_mode = ""
scroll_dir: Literal[-1, 1] = 1
scroll_start_ts: float = 0
hiss_scroll_up = False
control_mouse_forced = False
continuous_scrolling_speed_factor: float = 1.0
is_continuous_scrolling_vertical: bool = True

class ScrollingState:
    def __init__(self):
        self.continuous_scroll_mode = ""
        self.scroll_job = None
        self.scroll_dir: Literal[-1, 1] = 1
        self.scroll_start_ts: float = 0
        self.hiss_scroll_up = False
        self.control_mouse_forced = False
        self.continuous_scrolling_speed_factor: float = 1.0
        self.is_continuous_scrolling_vertical: bool = True
        self.continuously_scrolling: bool = False

    def start_continuous_scrolling_job(self):
        scroll_continuous_helper()
        scroll_job = cron.interval("16ms", scroll_continuous_helper)
        self.set_scrolling_job(scroll_job)
        self.continuously_scrolling = True

    def set_scrolling_job(self, job):
        self.stop_scrolling_job()
        self.scroll_job = job

    def stop_scrolling_job(self):
        if self.scroll_job:
            cron.cancel(self.scroll_job)
            self.scroll_job = None
        self.continuously_scrolling = False
        self.continuous_scrolling_speed_factor = 1.0

    def has_scrolling_job(self) -> bool:
        return self.scroll_job is not None

    def is_continuously_scrolling(self) -> bool:
        return self.continuously_scrolling

    def compute_scrolling_speed(self) -> int:
        scroll_amount = (
            settings.get("user.mouse_continuous_scroll_amount")
            * self.continuous_scrolling_speed_factor
        )
        acceleration_setting = settings.get("user.mouse_continuous_scroll_acceleration")
        acceleration_speed = (
            1 + min((time.perf_counter() - self.scroll_start_ts) / 0.5, acceleration_setting - 1)
            if acceleration_setting > 1
            else 1
        )

        scroll_delta = round(scroll_amount * acceleration_speed * scroll_dir)
        if scroll_delta == 0:
            scroll_delta = scroll_dir
        return scroll_delta

    def compute_gaze_scrolling_factor(self) -> float:
        return continuous_scrolling_speed_factor * settings.get(
        "user.mouse_gaze_scroll_speed_multiplier"
        )

    def set_continuous_scrolling_speed_factor(self, factor: float):
        self.continuous_scrolling_speed_factor = factor
        

scrolling_state = ScrollingState()

mod = Module()
ctx = Context()

mod.list(
    "continuous_scrolling_direction",
    desc="Defines names for directions used with continuous scrolling",
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

mod.setting(
    "mouse_continuous_scroll_speed_quotient",
    type=float,
    default=10.0,
    desc="When adjusting the continuous scrolling speed through voice commands, the result is that the speed is multiplied by the dictated number divided by this number.",
)

mod.setting(
    "mouse_gaze_scroll_speed_multiplier",
    type=float,
    default=1.0,
    desc="This multiplies the gaze scroll speed",
)

mod.tag(
    "continuous_scrolling",
    desc="Allows commands for adjusting continuous scrolling behavior",
)


@imgui.open(x=700, y=0)
def gui_wheel(gui: imgui.GUI):
    gui.text(f"Scroll mode: {continuous_scroll_mode}")
    gui.text(f"say a number between 0 and 99 to set scrolling speed")
    gui.line()
    if gui.button("[Wheel] Stop"):
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

    def mouse_scroll_continuous(direction: str, speed_factor: Optional[int] = None):
        """Scrolls continuously in the given direction"""
        match direction:
            case "UP":
                actions.user.mouse_scroll_up_continuous(speed_factor)
            case "DOWN":
                actions.user.mouse_scroll_down_continuous(speed_factor)
            case "LEFT":
                actions.user.mouse_scroll_left_continuous(speed_factor)
            case "RIGHT":
                actions.user.mouse_scroll_right_continuous(speed_factor)
            case _:
                raise ValueError(f"Invalid continuous scrolling direction: {direction}")

    def mouse_scroll_up_continuous(speed_factor: Optional[int] = None):
        """Scrolls up continuously"""
        mouse_scroll_continuous(-1, speed_factor)

    def mouse_scroll_down_continuous(speed_factor: Optional[int] = None):
        """Scrolls down continuously"""
        mouse_scroll_continuous(1, speed_factor)

    def mouse_scroll_right_continuous(speed_factor: Optional[int] = None):
        """Scrolls right continuously"""
        mouse_scroll_continuous(1, speed_factor, is_vertical=False)

    def mouse_scroll_left_continuous(speed_factor: Optional[int] = None):
        """Scrolls left continuously"""
        mouse_scroll_continuous(-1, speed_factor, is_vertical=False)

    def mouse_gaze_scroll():
        """Starts gaze scroll"""
        global continuous_scroll_mode, control_mouse_forced

        ctx.tags = ["user.continuous_scrolling"]

        continuous_scroll_mode = "gaze scroll"
        gaze_job = cron.interval("16ms", scroll_gaze_helper)
        scrolling_state.set_scrolling_job(gaze_job)

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
        global continuous_scroll_mode, control_mouse_forced

        continuous_scroll_mode = ""
        return_value = False
        ctx.tags = []
        
        if scrolling_state.has_scrolling_job():
            return_value = True
        scrolling_state.stop_scrolling_job()

        if control_mouse_forced:
            actions.tracking.control_toggle(False)
            control_mouse_forced = False

        gui_wheel.hide()

        return return_value

    def mouse_scroll_set_speed(speed: Optional[int]):
        """Sets the continuous scrolling speed for the current scrolling"""
        global scroll_start_ts
        if scroll_start_ts:
            scroll_start_ts = time.perf_counter()
        if speed is None:
            continuous_scrolling_speed_factor = 1.0
        else:
            continuous_scrolling_speed_factor = speed / settings.get(
                "user.mouse_continuous_scroll_speed_quotient"
            )
        scrolling_state.set_continuous_scrolling_speed_factor(continuous_scrolling_speed_factor)

    def mouse_is_continuous_scrolling():
        """Returns whether continuous scroll is in progress"""
        return scrolling_state.has_scrolling_job()

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


def mouse_scroll_continuous(
    new_scroll_dir: Literal[-1, 1],
    speed_factor: Optional[int] = None,
    is_vertical: bool = True,
):
    global scroll_dir, scroll_start_ts, is_continuous_scrolling_vertical
    actions.user.mouse_scroll_set_speed(speed_factor)
    was_vertical = is_continuous_scrolling_vertical
    is_continuous_scrolling_vertical = is_vertical

    update_continuous_scrolling_mode(new_scroll_dir, is_vertical)

    if scrolling_state.is_continuously_scrolling():
        # Issuing a scroll in the same direction aborts scrolling
        if scroll_dir == new_scroll_dir and was_vertical == is_vertical:
            actions.user.mouse_scroll_stop()
        # Issuing a scroll in the reverse direction resets acceleration
        else:
            scroll_dir = new_scroll_dir
            scroll_start_ts = time.perf_counter()
    else:
        scroll_dir = new_scroll_dir
        scroll_start_ts = time.perf_counter()
        scrolling_state.start_continuous_scrolling_job()
        ctx.tags = ["user.continuous_scrolling"]

        if not settings.get("user.mouse_hide_mouse_gui"):
            gui_wheel.show()


def update_continuous_scrolling_mode(new_scroll_dir: Literal[-1, 1], is_vertical: bool):
    global continuous_scroll_mode
    if new_scroll_dir == -1:
        if is_vertical:
            continuous_scroll_mode = "scroll up continuous"
        else:
            continuous_scroll_mode = "scroll left continuous"
    else:
        if is_vertical:
            continuous_scroll_mode = "scroll down continuous"
        else:
            continuous_scroll_mode = "scroll right continuous"


def scroll_continuous_helper():
    scroll_delta = scrolling_state.compute_scrolling_speed()
    if is_continuous_scrolling_vertical:
        actions.mouse_scroll(scroll_delta)
    else:
        actions.mouse_scroll(0, scroll_delta)


def scroll_gaze_helper():
    x, y = ctrl.mouse_pos()

    # The window containing the mouse
    window = get_window_containing(x, y)

    if window is None:
        return

    rect = window.rect
    midpoint = rect.center.y
    factor = scrolling_state.compute_gaze_scrolling_factor()
    amount = factor * (((y - midpoint) / (rect.height / 10)) ** 3)
    actions.mouse_scroll(amount)


def get_window_containing(x: float, y: float):
    # on windows, check the active_window first since ui.windows() is not z-ordered
    if app.platform == "windows" and ui.active_window().rect.contains(x, y):
        return ui.active_window()

    for window in ui.windows():
        if window.rect.contains(x, y):
            return window

    return None
