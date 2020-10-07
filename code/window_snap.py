"""Tools for voice-driven window management.

Originally from dweil/talon_community - modified for newapi by jcaw.

"""

# TODO: Map keyboard shortcuts to this manager once Talon has key hooks on all
#   platforms

import time
from operator import xor
from typing import Optional

from talon import ui, Module, Context, actions


def sorted_screens():
    """Return screens sorted by their topmost, then leftmost, edge.

    Screens will be sorted left-to-right, then top-to-bottom as a tiebreak.

    """

    return sorted(
        sorted(ui.screens(), key=lambda screen: screen.visible_rect.top),
        key=lambda screen: screen.visible_rect.left,
    )


def _set_window_pos(window, x, y, width, height):
    """Helper to set the window position."""
    # TODO: Special case for full screen move - use os-native maximize, rather
    #   than setting the position?

    # 2020/10/01: While the upstream Talon implementation for MS Windows is
    #   settling, this may be buggy on full screen windows. Aegis doesn't want a
    #   hacky solution merged, so for now just repeat the command.
    #
    # TODO: Audit once upstream Talon is bug-free on MS Windows
    window.rect = ui.Rect(round(x), round(y), round(width), round(height))


def _bring_forward(window):
    current_window = ui.active_window()
    try:
        window.focus()
        current_window.focus()
    except Exception as e:
        # We don't want to block if this fails.
        print(f"Couldn't bring window to front: {e}")


def _get_app_window(app_name: str) -> ui.Window:
    return actions.self.get_running_app(app_name).active_window


def _move_to_screen(
    window, offset: Optional[int] = None, screen_number: Optional[int] = None
):
    """Move a window to a different screen.

    Provide one of `offset` or `screen_number` to specify a target screen.

    Provide `window` to move a specific window, otherwise the current window is
    moved.

    """
    assert (
        screen_number or offset and not (screen_number and offset)
    ), "Provide exactly one of `screen_number` or `offset`."

    src_screen = window.screen
    screens = sorted_screens()
    if offset:
        screen_number = (screens.index(src_screen) + offset) % len(screens)
    else:
        # Human to array index
        screen_number -= 1

    dest_screen = screens[screen_number]
    if src_screen == dest_screen:
        return

    # Retain the same proportional position on the new screen.
    dest = dest_screen.visible_rect
    src = src_screen.visible_rect
    # TODO: Test this on different-sized screens
    #
    # TODO: Is this the best behaviour for moving to a vertical screen? Probably
    #   not.
    proportional_width = dest.width / src.width
    proportional_height = dest.height / src.height
    _set_window_pos(
        window,
        x=dest.left + (window.rect.left - src.left) * proportional_width,
        y=dest.top + (window.rect.top - src.top) * proportional_height,
        width=window.rect.width * proportional_width,
        height=window.rect.height * proportional_height,
    )


def _snap_window_helper(window, pos):
    screen = window.screen.visible_rect

    _set_window_pos(
        window,
        x=screen.x + (screen.width * pos.left),
        y=screen.y + (screen.height * pos.top),
        width=screen.width * (pos.right - pos.left),
        height=screen.height * (pos.bottom - pos.top),
    )


class RelativeScreenPos(object):
    """Represents a window position as a fraction of the screen."""

    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.bottom = bottom
        self.right = right


mod = Module()
mod.list(
    "window_snap_positions",
    "Predefined window positions for the current window. See `RelativeScreenPos`.",
)


_snap_positions = {
    # Halves
    # .---.---.     .-------.
    # |   |   |  &  |-------|
    # '---'---'     '-------'
    "left": RelativeScreenPos(0, 0, 0.5, 1),
    "right": RelativeScreenPos(0.5, 0, 1, 1),
    "top": RelativeScreenPos(0, 0, 1, 0.5),
    "bottom": RelativeScreenPos(0, 0.5, 1, 1),
    # Thirds
    # .--.--.--.
    # |  |  |  |
    # '--'--'--'
    "center third": RelativeScreenPos(1 / 3, 0, 2 / 3, 1),
    "left third": RelativeScreenPos(0, 0, 1 / 3, 1),
    "right third": RelativeScreenPos(2 / 3, 0, 1, 1),
    "left two thirds": RelativeScreenPos(0, 0, 2 / 3, 1),
    "right two thirds": RelativeScreenPos(1 / 3, 0, 1, 1,),
    # Quarters
    # .---.---.
    # |---|---|
    # '---'---'
    "top left": RelativeScreenPos(0, 0, 0.5, 0.5),
    "top right": RelativeScreenPos(0.5, 0, 1, 0.5),
    "bottom left": RelativeScreenPos(0, 0.5, 0.5, 1),
    "bottom right": RelativeScreenPos(0.5, 0.5, 1, 1),
    # Sixths
    # .--.--.--.
    # |--|--|--|
    # '--'--'--'
    "top right third": RelativeScreenPos(2 / 3, 0, 1, 0.5),
    "top left two thirds": RelativeScreenPos(0, 0, 2 / 3, 0.5),
    "top right two thirds": RelativeScreenPos(1 / 3, 0, 1, 0.5),
    "top center third": RelativeScreenPos(1 / 3, 0, 2 / 3, 0.5),
    "bottom left third": RelativeScreenPos(0, 0.5, 1 / 3, 1),
    "bottom right third": RelativeScreenPos(2 / 3, 0.5, 1, 1),
    "bottom left two thirds": RelativeScreenPos(0, 0.5, 2 / 3, 1),
    "bottom right two thirds": RelativeScreenPos(1 / 3, 0.5, 1, 1),
    "bottom center third": RelativeScreenPos(1 / 3, 0.5, 2 / 3, 1),
    # Special
    "center": RelativeScreenPos(1 / 8, 1 / 6, 7 / 8, 5 / 6),
    "full": RelativeScreenPos(0, 0, 1, 1),
    "fullscreen": RelativeScreenPos(0, 0, 1, 1),
}


@mod.capture(rule="{user.window_snap_positions}")
def window_snap_position(m) -> RelativeScreenPos:
    return _snap_positions[m.window_snap_positions]


ctx = Context()
ctx.lists["user.window_snap_positions"] = _snap_positions.keys()


@mod.action_class
class Actions:
    def snap_window(pos: RelativeScreenPos) -> None:
        """Move the active window to a specific position on-screen.

        See `RelativeScreenPos` for the structure of this position.

        """
        _snap_window_helper(ui.active_window(), pos)

    def move_window_next_screen() -> None:
        """Move the active window to a specific screen."""
        _move_to_screen(ui.active_window(), offset=1)

    def move_window_previous_screen() -> None:
        """Move the active window to the previous screen."""
        _move_to_screen(ui.active_window(), offset=-1)

    def move_window_to_screen(screen_number: int) -> None:
        """Move the active window leftward by one."""
        _move_to_screen(ui.active_window(), screen_number=screen_number)

    def snap_app(app_name: str, pos: RelativeScreenPos):
        """Snap a specific application to another screen."""
        window = _get_app_window(app_name)
        _bring_forward(window)
        _snap_window_helper(window, pos)

    def move_app_to_screen(app_name: str, screen_number: int):
        """Move a specific application to another screen."""
        window = _get_app_window(app_name)
        print(window)
        _bring_forward(window)
        _move_to_screen(
            window, screen_number=screen_number,
        )
