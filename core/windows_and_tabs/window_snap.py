"""Tools for voice-driven window management.

Originally from dweil/talon_community - modified for newapi by jcaw.

"""

# TODO: Map keyboard shortcuts to this manager once Talon has key hooks on all
#   platforms

import logging
from typing import Dict, Optional

from talon import Context, Module, actions, settings, ui
from talon.ui import Window

mod = Module()
mod.list(
    "window_snap_positions",
    "Predefined window positions for the current window. See `RelativeScreenPos`.",
)
mod.list(
    "window_split_positions",
    "Predefined window positions when splitting the screen between three applications.",
)
mod.setting(
    "window_snap_screen",
    type=str,
    default="proportional",
    desc="""How to position and size windows when snapping across different physical screens. Options:

  "proportional" (default): Preserve the window's relative position and size proportional to the screen.

  "size aware": Preserve position relative to the screen, but keep absolute size the same, except if window is full-height or -width, keep it so.
""",
)


def _set_window_pos(window, x, y, width, height):
    """Helper to set the window position."""
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


def interpolate_interval(w0, w1, s0, s1, d0, d1):
    """
    Interpolates an interval (w0, w1) which is within (s0, s1) so that it lies
    within (d0, d1). Returns (r0, r1). Tries to preserve absolute interval size,
    w1 - w0, while maintaining its relative 'position' within (s0, s1). For
    instance, if w0 == s0 then r0 == d0.

    Use-case: fix a window w, a source screen s, and a destination screen d.
    Let w0 = w.left, w1 = window.right, s0 = s.left, s1 = s.right, d0 = d.left, d1 = d.right.
    """
    wsize, ssize, dsize = w1 - w0, s1 - s0, d1 - d0
    assert wsize > 0 and ssize > 0 and dsize > 0
    before = max(0, (w0 - s0) / ssize)
    after = max(0, (s1 - w1) / ssize)
    # If we're within 5% of maximized, preserve this.
    if before + after <= 0.05:
        return (d0, d1)
    # If before is 0 (eg. window is left-aligned), we want to preserve before.
    # If after is 0 (eg. window is right-aligned), we want to preserve after.
    # In between, we linearly interpolate.
    beforeness = before / (before + after)
    afterness = after / (before + after)
    a0, b1 = d0 + before * dsize, d1 - after * dsize
    a1, b0 = a0 + wsize, b1 - wsize
    r0 = a0 * afterness + b0 * beforeness
    r1 = a1 * afterness + b1 * beforeness
    return (max(d0, r0), min(d1, r1))  # clamp to destination


def _move_to_screen(
    window: ui.Window, offset: Optional[int] = None, screen_number: Optional[int] = None
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

    if offset:
        if offset < 0:
            dest_screen = actions.user.screens_get_previous(src_screen)
        else:
            dest_screen = actions.user.screens_get_next(src_screen)
    else:
        dest_screen = actions.user.screens_get_by_number(screen_number)

    if src_screen == dest_screen:
        return

    dest = dest_screen.visible_rect
    src = src_screen.visible_rect
    maximized = window.maximized
    how = settings.get("user.window_snap_screen")
    if how == "size aware":
        r = window.rect
        left, right = interpolate_interval(
            r.left, r.right, src.left, src.right, dest.left, dest.right
        )
        top, bot = interpolate_interval(
            r.top, r.bot, src.top, src.bot, dest.top, dest.bot
        )
        r.x, r.y = left, top
        r.width = right - left
        r.height = bot - top
        window.rect = r
        if maximized:
            window.maximized = True
        return

    # TODO: Test vertical screen with different aspect ratios
    # Does the orientation between the screens change? (vertical/horizontal)
    if how != "proportional":
        logging.warning(
            f"Unrecognized 'window_snap_screen' setting: {how!r}. Using default 'proportional'."
        )
    if (src.width / src.height > 1) != (dest.width / dest.height > 1):
        # Horizontal -> vertical or vertical -> horizontal
        # Retain proportional window size, but flip x/y of the vertical monitor to account for the monitors rotation.
        if src.width / src.height > 1:
            # horizontal -> vertical
            width = window.rect.width * dest.height / src.width
            height = window.rect.height * dest.width / src.height
        else:
            # vertical -> horizontal
            width = window.rect.width * dest.width / src.height
            height = window.rect.height * dest.height / src.width
        # Deform window if width or height is bigger than the target monitors while keeping the window area the same.
        if width > dest.width:
            over = (width - dest.width) * height
            width = dest.width
            height += over / width
        if height > dest.height:
            over = (height - dest.height) * width
            height = dest.height
            width += over / height
        # Proportional position:
        # Since the window size in respect to the monitor size is not proportional (x/y was flipped),
        # the positioning is more complicated than proportionally scaling the x/y coordinates.
        # It is computed by keeping the free space to the left of the window proportional to the right
        # and respectively for the top/bottom free space.
        # The if conditions account for division by 0. TODO: Refactor positioning without division by 0
        if src.height == window.rect.height:
            x = dest.left + (dest.width - width) / 2
        else:
            x = dest.left + (window.rect.top - src.top) * (dest.width - width) / (
                src.height - window.rect.height
            )
        if src.width == window.rect.width:
            y = dest.top + (dest.height - height) / 2
        else:
            y = dest.top + (window.rect.left - src.left) * (dest.height - height) / (
                src.width - window.rect.width
            )
    else:
        # Horizontal -> horizontal or vertical -> vertical
        # Retain proportional size and position
        proportional_width = dest.width / src.width
        proportional_height = dest.height / src.height
        x = dest.left + (window.rect.left - src.left) * proportional_width
        y = dest.top + (window.rect.top - src.top) * proportional_height
        width = window.rect.width * proportional_width
        height = window.rect.height * proportional_height
    _set_window_pos(window, x=x, y=y, width=width, height=height)
    if maximized:
        window.maximized = True


def _snap_window_helper(window, pos):
    screen = window.screen.visible_rect

    _set_window_pos(
        window,
        x=screen.x + (screen.width * pos.left),
        y=screen.y + (screen.height * pos.top),
        width=screen.width * (pos.right - pos.left),
        height=screen.height * (pos.bottom - pos.top),
    )


class RelativeScreenPos:
    """Represents a window position as a fraction of the screen."""

    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.bottom = bottom
        self.right = right

    def __str__(self):
        return f"RelativeScreenPos(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"


_snap_positions = {
    # Halves
    # .---.---.     .-------.
    # |   |   |  &  |-------|
    # '---'---'     '-------'
    "LEFT": RelativeScreenPos(0, 0, 0.5, 1),
    "RIGHT": RelativeScreenPos(0.5, 0, 1, 1),
    "TOP": RelativeScreenPos(0, 0, 1, 0.5),
    "BOTTOM": RelativeScreenPos(0, 0.5, 1, 1),
    # Thirds
    # .--.--.--.
    # |  |  |  |
    # '--'--'--'
    "CENTER_THIRD": RelativeScreenPos(1 / 3, 0, 2 / 3, 1),
    "LEFT_THIRD": RelativeScreenPos(0, 0, 1 / 3, 1),
    "RIGHT_THIRD": RelativeScreenPos(2 / 3, 0, 1, 1),
    "LEFT_TWO_THIRDS": RelativeScreenPos(0, 0, 2 / 3, 1),
    "RIGHT_TWO_THIRDS": RelativeScreenPos(1 / 3, 0, 1, 1),
    # Alternate (simpler) spoken forms for thirds
    "CENTER_SMALL": RelativeScreenPos(1 / 3, 0, 2 / 3, 1),
    "LEFT_SMALL": RelativeScreenPos(0, 0, 1 / 3, 1),
    "RIGHT_SMALL": RelativeScreenPos(2 / 3, 0, 1, 1),
    "LEFT_LARGE": RelativeScreenPos(0, 0, 2 / 3, 1),
    "RIGHT_LARGE": RelativeScreenPos(1 / 3, 0, 1, 1),
    # Quarters
    # .---.---.
    # |---|---|
    # '---'---'
    "TOP_LEFT": RelativeScreenPos(0, 0, 0.5, 0.5),
    "TOP_RIGHT": RelativeScreenPos(0.5, 0, 1, 0.5),
    "BOTTOM_LEFT": RelativeScreenPos(0, 0.5, 0.5, 1),
    "BOTTOM_RIGHT": RelativeScreenPos(0.5, 0.5, 1, 1),
    # Sixths
    # .--.--.--.
    # |--|--|--|
    # '--'--'--'
    "TOP_LEFT_THIRD": RelativeScreenPos(0, 0, 1 / 3, 0.5),
    "TOP_RIGHT_THIRD": RelativeScreenPos(2 / 3, 0, 1, 0.5),
    "TOP_LEFT_TWO_THIRDS": RelativeScreenPos(0, 0, 2 / 3, 0.5),
    "TOP_RIGHT_TWO_THIRDS": RelativeScreenPos(1 / 3, 0, 1, 0.5),
    "TOP_CENTER_THIRD": RelativeScreenPos(1 / 3, 0, 2 / 3, 0.5),
    "BOTTOM_LEFT_THIRD": RelativeScreenPos(0, 0.5, 1 / 3, 1),
    "BOTTOM_RIGHT_THIRD": RelativeScreenPos(2 / 3, 0.5, 1, 1),
    "BOTTOM_LEFT_TWO_THIRDS": RelativeScreenPos(0, 0.5, 2 / 3, 1),
    "BOTTOM_RIGHT_TWO_THIRDS": RelativeScreenPos(1 / 3, 0.5, 1, 1),
    "BOTTOM_CENTER_THIRD": RelativeScreenPos(1 / 3, 0.5, 2 / 3, 1),
    # Alternate (simpler) spoken forms for sixths
    "TOP_LEFT_SMALL": RelativeScreenPos(0, 0, 1 / 3, 0.5),
    "TOP_RIGHT_SMALL": RelativeScreenPos(2 / 3, 0, 1, 0.5),
    "TOP_LEFT_LARGE": RelativeScreenPos(0, 0, 2 / 3, 0.5),
    "TOP_RIGHT_LARGE": RelativeScreenPos(1 / 3, 0, 1, 0.5),
    "TOP_CENTER_SMALL": RelativeScreenPos(1 / 3, 0, 2 / 3, 0.5),
    "BOTTOM_LEFT_SMALL": RelativeScreenPos(0, 0.5, 1 / 3, 1),
    "BOTTOM_RIGHT_SMALL": RelativeScreenPos(2 / 3, 0.5, 1, 1),
    "BOTTOM_LEFT_LARGE": RelativeScreenPos(0, 0.5, 2 / 3, 1),
    "BOTTOM_RIGHT_LARGE": RelativeScreenPos(1 / 3, 0.5, 1, 1),
    "BOTTOM_CENTER_SMALL": RelativeScreenPos(1 / 3, 0.5, 2 / 3, 1),
    # Special
    "CENTER": RelativeScreenPos(1 / 8, 1 / 6, 7 / 8, 5 / 6),
    "FULL": RelativeScreenPos(0, 0, 1, 1),
    "FULLSCREEN": RelativeScreenPos(0, 0, 1, 1),
}
_split_positions = {
    "split": {
        2: [_snap_positions["LEFT"], _snap_positions["RIGHT"]],
        3: [
            _snap_positions["LEFT_THIRD"],
            _snap_positions["CENTER_THIRD"],
            _snap_positions["RIGHT_THIRD"],
        ],
    },
    "clock": {
        3: [
            _snap_positions["LEFT"],
            _snap_positions["TOP_RIGHT"],
            _snap_positions["BOTTOM_RIGHT"],
        ],
    },
    "counterclock": {
        3: [
            _snap_positions["RIGHT"],
            _snap_positions["TOP_LEFT"],
            _snap_positions["BOTTOM_LEFT"],
        ],
    },
}


@mod.capture(rule="{user.window_snap_positions}")
def window_snap_position(m) -> RelativeScreenPos:
    return _snap_positions[m.window_snap_positions]


@mod.capture(rule="{user.window_split_positions}")
def window_split_position(m) -> Dict[int, list[RelativeScreenPos]]:
    return _split_positions[m.window_split_positions]


ctx = Context()
ctx.lists["user.window_snap_positions"] = _snap_positions.keys()
ctx.lists["user.window_split_positions"] = _split_positions.keys()


@mod.action_class
class Actions:
    def snap_window(
        position: RelativeScreenPos, window: Optional[Window] = None
    ) -> None:
        """Move a window (defaults to the active window) to a specific position on its current screen, given a `RelativeScreenPos` object."""
        if window is None:
            window = ui.active_window()
        _snap_window_helper(window, position)

    def snap_window_to_position(
        position_name: str, window: Optional[Window] = None
    ) -> None:
        """Move a window (defaults to the active window) to a specifically named position on its current screen, using a key from `_snap_positions`."""
        position: Optional[RelativeScreenPos] = None
        if position_name in _snap_positions:
            position = _snap_positions[position_name]
            actions.user.snap_window(position, window)
        else:
            # Previously this function took a spoken form, but we now have constant identifiers in `_snap_positions`.
            # If the user passed a previous spoken form instead, see if we can convert it to the new identifier.
            new_key = actions.user.formatted_text(position_name, "ALL_CAPS,SNAKE_CASE")
            if new_key in _snap_positions:
                actions.user.deprecate_action(
                    "2024-12-02",
                    f"snap_window_to_position('{position_name}')",
                    f"snap_window_to_position('{new_key}')",
                )
                position = _snap_positions[new_key]
                actions.user.snap_window(position, window)
            else:
                raise KeyError(position_name)

    def move_window_next_screen() -> None:
        """Move the active window to a specific screen."""
        _move_to_screen(ui.active_window(), offset=1)

    def move_window_previous_screen() -> None:
        """Move the active window to the previous screen."""
        _move_to_screen(ui.active_window(), offset=-1)

    def move_window_to_screen(screen_number: int) -> None:
        """Move the active window leftward by one."""
        _move_to_screen(ui.active_window(), screen_number=screen_number)

    def snap_app(app_name: str, position: RelativeScreenPos):
        """Snap a specific application to another screen."""
        window = _get_app_window(app_name)
        _bring_forward(window)
        _snap_window_helper(window, position)

    def snap_layout(
        positions_by_count: Dict[int, list[RelativeScreenPos]],
        apps: list[str],
    ):
        """Split the screen between multiple applications."""
        try:
            positions = positions_by_count[len(apps)]
        except KeyError:
            supported_layouts = ", ".join(map(str, positions_by_count.keys()))
            message = f"{len(apps)} applications given but chosen layout only supports {supported_layouts}"
            actions.app.notify(message, "Cannot arrange")
            raise NotImplementedError(message)
        for index, app in enumerate(apps):
            window = _get_app_window(app)
            _snap_window_helper(window, positions[index])
            window.focus()

    def move_app_to_screen(app_name: str, screen_number: int):
        """Move a specific application to another screen."""
        window = _get_app_window(app_name)
        _bring_forward(window)
        _move_to_screen(
            window,
            screen_number=screen_number,
        )
