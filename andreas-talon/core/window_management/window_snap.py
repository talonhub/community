from talon import ui, Module, Context, actions
from talon.types import Rect
from dataclasses import dataclass
from typing import Union


@dataclass
class RelativePosition:
    """Represents a window position as a fraction of the screen."""

    left: float
    top: float
    right: float
    bottom: float


snap_positions = {
    # Halves
    # .---.---.     .-------.
    # |   |   |  &  |-------|
    # '---'---'     '-------'
    "left": RelativePosition(0, 0, 0.5, 1),
    "right": RelativePosition(0.5, 0, 1, 1),
    "top": RelativePosition(0, 0, 1, 0.5),
    "bottom": RelativePosition(0, 0.5, 1, 1),
    # Thirds
    # .--.--.--.
    # |  |  |  |
    # '--'--'--'
    "left small": RelativePosition(0, 0, 1 / 3, 1),
    "center small": RelativePosition(1 / 3, 0, 2 / 3, 1),
    "right small": RelativePosition(2 / 3, 0, 1, 1),
    "left large": RelativePosition(0, 0, 2 / 3, 1),
    "right large": RelativePosition(1 / 3, 0, 1, 1),
    # Quarters
    # .---.---.
    # |---|---|
    # '---'---'
    "top left": RelativePosition(0, 0, 0.5, 0.5),
    "top right": RelativePosition(0.5, 0, 1, 0.5),
    "bottom left": RelativePosition(0, 0.5, 0.5, 1),
    "bottom right": RelativePosition(0.5, 0.5, 1, 1),
    # Sixths
    # .--.--.--.
    # |--|--|--|
    # '--'--'--'
    "top left small": RelativePosition(0, 0, 1 / 3, 0.5),
    "top center small": RelativePosition(1 / 3, 0, 2 / 3, 0.5),
    "top right small": RelativePosition(2 / 3, 0, 1, 0.5),
    "bottom left small": RelativePosition(0, 0.5, 1 / 3, 1),
    "bottom center small": RelativePosition(1 / 3, 0.5, 2 / 3, 1),
    "bottom right small": RelativePosition(2 / 3, 0.5, 1, 1),
    "top left large": RelativePosition(0, 0, 2 / 3, 0.5),
    "top right large": RelativePosition(1 / 3, 0, 1, 0.5),
    "bottom left large": RelativePosition(0, 0.5, 2 / 3, 1),
    "bottom right large": RelativePosition(1 / 3, 0.5, 1, 1),
    # Special
    "center": RelativePosition(1 / 6, 0, 5 / 6, 1),
    "top center": RelativePosition(1 / 6, 0, 5 / 6, 0.5),
    "bottom center": RelativePosition(1 / 6, 0.5, 5 / 6, 1),
    "middle": RelativePosition(1 / 6, 1 / 8, 5 / 6, 1),
    "full": RelativePosition(0, 0, 1, 1),
}

mod = Module()
ctx = Context()

mod.list(
    "snap_position",
    "Predefined window positions for the current window. See `RelativePosition`.",
)
ctx.lists["user.snap_position"] = snap_positions.keys()


@mod.capture(rule="last | next")
def prev_next(m) -> str:
    "Previous or next position"
    return "previous" if "last" == m[0] else "next"


@mod.capture(
    rule="<user.prev_next> screen | screen (<user.prev_next> | <number_small>)"
)
def snap_screen(m) -> Union[int, str]:
    "A single screen position."
    try:
        return m.number_small
    except AttributeError:
        return m.prev_next


@mod.action_class
class Actions:
    def snap_active_window_to_screen(screen_desc: Union[int, str]):
        """Move the active window to screen <screen_desc> while retaining the same relative position"""
        snap_window_to_screen(
            ui.active_window(),
            get_screen(screen_desc),
        )

    def snap_window_under_cursor_to_screen(screen_desc: Union[int, str]):
        """Move the window under the cursor to screen <screen_desc> while retaining the same relative position"""
        snap_window_to_screen(
            actions.user.get_window_under_cursor(),
            get_screen(screen_desc),
        )

    def snap_application_to_screen(
        app_name: str,
        screen_desc: Union[int, str],
    ):
        """Move window for application <app_name> to screen <screen_desc> while retaining the same relative position"""
        snap_window_to_screen(
            actions.user.get_app_window(app_name),
            get_screen(screen_desc),
        )

    def snap_active_window_to_position(pos_name: str):
        """Move the active window to position <pos_name> on the current screen"""
        window = ui.active_window()
        snap_window_to_screen_and_position(
            window,
            window.screen,
            pos_name,
        )

    def snap_window_under_cursor_to_position(pos_name: str):
        """Move the window under the cursor to position <pos_name> on the current screen"""
        window = actions.user.get_window_under_cursor()
        snap_window_to_screen_and_position(
            window,
            window.screen,
            pos_name,
        )

    def snap_application_to_position(
        app_name: str,
        pos_name: str,
    ):
        """Move window for application <app_name> to position <pos_name> on the current screen"""
        window = actions.user.get_app_window(app_name)
        snap_window_to_screen_and_position(
            window,
            window.screen,
            pos_name,
        )

    def snap_active_window_to_screen_and_position(
        screen_desc: Union[int, str],
        pos_name: str,
    ):
        """Move the active window to position <pos_name> on screen <screen_desc>"""
        print(ui.active_window())
        snap_window_to_screen_and_position(
            ui.active_window(),
            get_screen(screen_desc),
            pos_name,
        )

    def snap_window_under_cursor_to_screen_and_position(
        screen_desc: Union[int, str],
        pos_name: str,
    ):
        """Move the window under the cursor to position <pos_name> on screen <screen_desc>"""
        snap_window_to_screen_and_position(
            actions.user.get_window_under_cursor(),
            get_screen(screen_desc),
            pos_name,
        )
    def snap_specified_window_to_position(
        window: ui.Window, 
        pos_name: str,
    ):
        """Move the active window to position <pos_name> on screen <screen_desc>"""
        snap_window_to_screen_and_position(
            window, 
            window.screen, 
            pos_name,
        )

    def snap_application_to_screen_and_position(
        app_name: str,
        screen_desc: Union[int, str],
        pos_name: str,
    ):
        """Move window for application <app_name> to position <pos_name> on screen <screen_desc>"""
        snap_window_to_screen_and_position(
            actions.user.get_app_window(app_name),
            get_screen(screen_desc),
            pos_name,
        )

    def snap_apply_position_to_rect(rect: Rect, pos_name: str) -> Rect:
        """Applies snap position <pos_name> to given rectangle"""
        pos = snap_positions[pos_name]
        return Rect(
            rect.x + (rect.width * pos.left),
            rect.y + (rect.height * pos.top),
            rect.width * (pos.right - pos.left),
            rect.height * (pos.bottom - pos.top),
        )


def snap_window_to_screen(window: ui.Window, screen: ui.Screen):
    dest = screen.visible_rect
    src = window.screen.visible_rect
    proportional_width = dest.width / src.width
    proportional_height = dest.height / src.height
    actions.user.window_set_pos(
        window,
        x=dest.left + (window.rect.left - src.left) * proportional_width,
        y=dest.top + (window.rect.top - src.top) * proportional_height,
        width=window.rect.width * proportional_width,
        height=window.rect.height * proportional_height,
    )
    


def snap_window_to_screen_and_position(
    window: ui.Window, screen: ui.Screen, pos_name: str
):
    rect = actions.user.snap_apply_position_to_rect(screen.visible_rect, pos_name)
    actions.user.window_set_pos(window, rect.x, rect.y, rect.width, rect.height)


def get_screen(screen_desc: Union[int, str]) -> ui.Screen:
    if screen_desc == "previous":
        return actions.user.screen_get_by_offset(-1)
    if screen_desc == "next":
        return actions.user.screen_get_by_offset(1)
    return actions.user.screens_get_by_number(screen_desc)
