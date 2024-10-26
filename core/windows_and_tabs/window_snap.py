"""Tools for voice-driven window management.

Originally from dweil/talon_community - modified for newapi by jcaw.

"""

# TODO: Map keyboard shortcuts to this manager once Talon has key hooks on all
#   platforms

import logging
from typing import Any, Dict, Optional

from talon import Context, Module, actions, settings, ui

mod = Module()
mod.list(
    "window_snap_positions",
    "Predefined window positions for the current window. See `RelativeScreenPos`.",
)
mod.list(
    "window_split_positions",
    "Predefined window positions when splitting the screen between multiple windows.",
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
last_focus_was_done_by_snap_layout = False
currently_snapping_layout = False


def _focus_was_done_by_other_method(_):
    global last_focus_was_done_by_snap_layout
    global currently_snapping_layout

    if not currently_snapping_layout:
        print("Resetting last focus")
        last_focus_was_done_by_snap_layout = False


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
        # Return a string representation of the RelativeScreenPos instance
        return f"RelativeScreenPos(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"


class WindowLayout:
    """Represents a layout of windows on a screen"""

    def __init__(
        self, layout: list[RelativeScreenPos], windows: list[Any], should_rotate: bool
    ):
        self.layout = layout
        self.windows = windows
        self.should_rotate = should_rotate


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
    "right two thirds": RelativeScreenPos(1 / 3, 0, 1, 1),
    # Alternate (simpler) spoken forms for thirds
    "center small": RelativeScreenPos(1 / 3, 0, 2 / 3, 1),
    "left small": RelativeScreenPos(0, 0, 1 / 3, 1),
    "right small": RelativeScreenPos(2 / 3, 0, 1, 1),
    "left large": RelativeScreenPos(0, 0, 2 / 3, 1),
    "right large": RelativeScreenPos(1 / 3, 0, 1, 1),
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
    "top left third": RelativeScreenPos(0, 0, 1 / 3, 0.5),
    "top right third": RelativeScreenPos(2 / 3, 0, 1, 0.5),
    "top left two thirds": RelativeScreenPos(0, 0, 2 / 3, 0.5),
    "top right two thirds": RelativeScreenPos(1 / 3, 0, 1, 0.5),
    "top center third": RelativeScreenPos(1 / 3, 0, 2 / 3, 0.5),
    "bottom left third": RelativeScreenPos(0, 0.5, 1 / 3, 1),
    "bottom right third": RelativeScreenPos(2 / 3, 0.5, 1, 1),
    "bottom left two thirds": RelativeScreenPos(0, 0.5, 2 / 3, 1),
    "bottom right two thirds": RelativeScreenPos(1 / 3, 0.5, 1, 1),
    "bottom center third": RelativeScreenPos(1 / 3, 0.5, 2 / 3, 1),
    # Alternate (simpler) spoken forms for sixths
    "top left small": RelativeScreenPos(0, 0, 1 / 3, 0.5),
    "top right small": RelativeScreenPos(2 / 3, 0, 1, 0.5),
    "top left large": RelativeScreenPos(0, 0, 2 / 3, 0.5),
    "top right large": RelativeScreenPos(1 / 3, 0, 1, 0.5),
    "top center small": RelativeScreenPos(1 / 3, 0, 2 / 3, 0.5),
    "bottom left small": RelativeScreenPos(0, 0.5, 1 / 3, 1),
    "bottom right small": RelativeScreenPos(2 / 3, 0.5, 1, 1),
    "bottom left large": RelativeScreenPos(0, 0.5, 2 / 3, 1),
    "bottom right large": RelativeScreenPos(1 / 3, 0.5, 1, 1),
    "bottom center small": RelativeScreenPos(1 / 3, 0.5, 2 / 3, 1),
    # Special
    "center": RelativeScreenPos(1 / 8, 1 / 6, 7 / 8, 5 / 6),
    "full": RelativeScreenPos(0, 0, 1, 1),
    "fullscreen": RelativeScreenPos(0, 0, 1, 1),
}

_split_positions = {
    "split": {
        2: [_snap_positions["left"], _snap_positions["right"]],
        3: [
            _snap_positions["left third"],
            _snap_positions["center third"],
            _snap_positions["right third"],
        ],
    },
    "clock": {
        3: [
            _snap_positions["left"],
            _snap_positions["top right"],
            _snap_positions["bottom right"],
        ],
    },
    "counterclock": {
        3: [
            _snap_positions["right"],
            _snap_positions["top left"],
            _snap_positions["bottom left"],
        ],
    },
}


def _snap_next(windows: list[Any], target_layout: RelativeScreenPos) -> Optional[int]:
    print(windows)
    for index, window in enumerate(windows):
        if window is None:
            return index
        try:
            _snap_window_helper(
                window,
                target_layout,
            )
            return index
        except Exception as e:
            print(f"Failed to snap window: {e}")
    return None


def _snap_layout(window_layout: WindowLayout):
    """Split the screen between multiple windows."""
    global last_focus_was_done_by_snap_layout
    global currently_snapping_layout
    currently_snapping_layout = True
    import copy

    target_layout = copy.deepcopy(window_layout.layout)
    remaining_windows = window_layout.windows
    snapped_windows = []
    snapped_window_index = 0
    if window_layout.should_rotate:
        print("Trying to rotate")
        target_layout.append(target_layout.pop(0))

    while len(target_layout) > 0:
        snapped_window_index = _snap_next(remaining_windows, target_layout.pop(0))
        if snapped_window_index is not None:
            snapped_windows.insert(0, remaining_windows[snapped_window_index])
            remaining_windows = remaining_windows[snapped_window_index + 1 :]

    if window_layout.should_rotate and len(snapped_windows) > 0:
        snapped_windows.append(snapped_windows.pop(0))
    for window in snapped_windows:
        window.focus()
        actions.sleep("180ms")
    actions.sleep("500ms")
    last_focus_was_done_by_snap_layout = True
    currently_snapping_layout = False


def _top_n_windows() -> list[Any]:
    active_window = ui.active_window()
    ui_windows = ui.windows()
    try:
        active_index = ui_windows.index(active_window)
        return ui_windows[active_index:]
    except Exception:
        return ui_windows


@mod.capture(rule="{user.window_snap_positions}")
def window_snap_position(m) -> RelativeScreenPos:
    return _snap_positions[m.window_snap_positions]


@mod.capture(rule="{user.window_split_positions} [<number_small>]")
def window_split_position(m) -> list[RelativeScreenPos]:
    if hasattr(m, "number_small"):
        return _split_positions[m.window_split_positions][m.number_small]
    else:
        min_key = min(_split_positions[m.window_split_positions].keys())
        return _split_positions[m.window_split_positions][min_key]


@mod.capture(rule="all")
def all_windows(m) -> list[Any]:
    return _top_n_windows()


@mod.capture(rule="gap")
def skip_window(m) -> list[Any]:
    return [None]


@mod.capture(rule="<user.running_applications>")
def application_windows(m) -> list[Any]:
    return [
        window
        for app in m.running_applications_list
        for window in actions.self.get_running_app(app).windows()
    ]


@mod.capture(
    rule="<user.application_windows>|<user.numbered_windows>|<user.skip_window>"
)
def layout_item(m) -> list[Any]:
    # Check for multiple attributes and raise an error if found
    attributes = [
        hasattr(m, "application_windows"),
        hasattr(m, "numbered_windows"),
        hasattr(m, "skip_window"),
    ]

    if sum(attributes) > 1:
        raise ValueError(
            "Multiple attributes found on 'm'. Only one of 'application_windows', 'numbered_windows', or 'skip_window' should be present."
        )

    # Return the appropriate list based on which attribute is available
    if hasattr(m, "application_windows"):
        return m.application_windows
    elif hasattr(m, "numbered_windows"):
        return m.numbered_windows
    elif hasattr(m, "skip_window"):
        return m.skip_window
    else:
        return []


@mod.capture(rule="<user.ordinals_small>+")
def numbered_windows(m) -> list[Any]:
    all_windows = _top_n_windows()
    selected_windows = [
        all_windows[i - 1] for i in m.ordinals_small_list if i - 1 < len(all_windows)
    ]
    return selected_windows


@mod.capture(rule="<user.layout_item>+ [<user.all_windows>]")
def target_windows(m) -> list[Any]:
    windows = []
    if hasattr(m, "layout_item_list"):
        windows += [window for sublist in m.layout_item_list for window in sublist]

    if hasattr(m, "all_windows"):
        windows += [w for w in m.all_windows if w not in windows]
    return windows


@mod.capture(
    rule="{user.window_split_positions} [<number_small>] [<user.target_windows>]"
)
def window_layout(m) -> WindowLayout:
    global last_focus_was_done_by_snap_layout
    if hasattr(m, "target_windows"):
        target_length = len(m.target_windows)
    else:
        target_length = len(_top_n_windows())
    if hasattr(m, "number_small"):
        layout = _split_positions[m.window_split_positions][m.number_small]
    else:
        closest_key = min(
            _split_positions[m.window_split_positions].keys(),
            key=lambda k: abs(k - target_length),
        )
        layout = _split_positions[m.window_split_positions][closest_key]
    if hasattr(m, "target_windows"):
        target_windows = m.target_windows
    else:
        target_windows = _top_n_windows()

    return WindowLayout(
        layout,
        target_windows,
        not hasattr(m, "target_windows") and last_focus_was_done_by_snap_layout,
    )


ctx = Context()
ctx.lists["user.window_snap_positions"] = _snap_positions.keys()
ctx.lists["user.window_split_positions"] = _split_positions.keys()


@mod.action_class
class Actions:
    def snap_window(position: RelativeScreenPos) -> None:
        """Move the active window to a specific position on its current screen, given a `RelativeScreenPos` object."""
        _snap_window_helper(ui.active_window(), position)

    def snap_window_to_position(position_name: str) -> None:
        """Move the active window to a specifically named position on its current screen, using a key from `_snap_positions`."""
        actions.user.snap_window(_snap_positions[position_name])

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
        window_layout: WindowLayout,
    ):
        """Split the screen between multiple applications."""
        _snap_layout(window_layout)

    def move_app_to_screen(app_name: str, screen_number: int):
        """Move a specific application to another screen."""
        window = _get_app_window(app_name)
        _bring_forward(window)
        _move_to_screen(
            window,
            screen_number=screen_number,
        )


ui.register("app_activate", _focus_was_done_by_other_method)
ui.register("win_focus", _focus_was_done_by_other_method)
