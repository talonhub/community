import copy
import time
from dataclasses import dataclass
from typing import List, Optional, Union

from talon import Context, Module, actions, settings, ui
from talon.ui import UIErr, Window

from .windows_and_tabs import is_window_valid

"""Tools for laying out windows in an arrangement """

SPLIT_POSITIONS = {
    # Explicit layout names with only one configuration can be easier to force
    # the desired result:
    "HALVES": ["LEFT", "RIGHT"],
    "THIRDS": ["LEFT_THIRD", "CENTER_THIRD", "RIGHT_THIRD"],
    "CLOCK": [
        "LEFT",
        "TOP_RIGHT",
        "BOTTOM_RIGHT",
    ],
    "COUNTERCLOCK": [
        "RIGHT",
        "TOP_LEFT",
        "BOTTOM_LEFT",
    ],
    "GRID": [
        "TOP_LEFT",
        "TOP_RIGHT",
        "BOTTOM_LEFT",
        "BOTTOM_RIGHT",
    ],
    "BIG_GRID": [
        "TOP_LEFT_THIRD",
        "TOP_CENTER_THIRD",
        "TOP_RIGHT_THIRD",
        "BOTTOM_LEFT_THIRD",
        "BOTTOM_CENTER_THIRD",
        "BOTTOM_RIGHT_THIRD",
    ],
}

# Keys in `windows_snap.py` `_snap_positions`, ie "TopLeft", "BottomCenterThird", etc.
SnapPosition = str


@dataclass
class WindowLayout:
    """Represents a layout of windows on a screen"""

    name: str
    split_positions: list[SnapPosition]
    windows: list[Window]
    can_rotate: bool
    rotation_count: int
    finish_time: float


class Gap:
    """Users can leave gaps or holes (as in a code snippet) when dictating a layout;
    this represents such a gap."""

    pass


# Create a union type for Talon windows and Gaps:
Window = Union[Window, Gap]

# The current layout being arranged and the last one arranged, if any.
layout_in_progress: Optional[WindowLayout] = None
last_layout: Optional[WindowLayout] = None


def snap_next(windows: list[Window], target_layout: SnapPosition) -> Optional[Window]:
    """This function snaps a window and returns the window if successful"""
    while windows:
        window = windows.pop(0)
        if isinstance(window, Gap):
            return window
        try:
            actions.user.snap_window_to_position(
                target_layout,
                window,
            )

            return window
        except (UIErr, AttributeError) as e:
            print(
                f'Failed to snap {window.app.name}\'s "{window.title}" window ({type(e).__name__} {e}); this is normal; continuing to the next'
            )
    return Gap()


def snap_layout(layout: WindowLayout):
    """Split the screen between multiple windows."""
    try:
        global layout_in_progress, last_layout
        layout_in_progress = layout

        # If called multiple times (and the user hasn't focused a window manually since
        # last time), rotate the offset of the existing windows in the arrangement,
        # allowing the user to use a repeater to cycle through the windows to get the
        # desired result.
        if (
            layout.can_rotate
            and last_layout is not None
            and last_layout.name == layout.name
            and layout.windows == last_layout.windows
        ):
            layout.rotation_count = last_layout.rotation_count + 1

        # Copy these data structures so we can mutate them:
        remaining_windows = [w for w in layout.windows]
        split_positions = layout.split_positions.copy()

        snapped_windows = []
        for _ in range(layout.rotation_count):
            split_positions.append(split_positions.pop(0))

        while len(split_positions) > 0:
            snapped_window: Window = snap_next(
                remaining_windows, split_positions.pop(0)
            )
            snapped_windows.insert(0, snapped_window)

        if len(snapped_windows) > 0:
            for _ in range(layout.rotation_count):
                snapped_windows.append(snapped_windows.pop(0))

        for window in snapped_windows:
            if isinstance(window, Gap):
                continue
            actions.user.switcher_focus_window(window)

        layout_in_progress.finish_time = time.perf_counter()
        last_layout = layout_in_progress
    finally:
        layout_in_progress = None


def filter_nonviable_windows(windows: List[Window]) -> list[Window]:
    active_window = ui.active_window()

    # Many invisible non-resizable windows are identifiable because they exist above the current window
    # in the z-index
    all_windows = ui.windows()
    active_window_idx = all_windows.index(active_window)  # type: ignore
    return list(
        filter(
            lambda w: (isinstance(w, Gap) or is_window_valid(w)),
            windows,
        )
    )


mod = Module()
mod.list(
    "window_split_positions",
    "Predefined window positions when splitting the screen between multiple windows.",
)
mod.tag(
    "experimental_window_layout",
    desc="Tag to enable experimental window layout commands",
)

ctx = Context()


@mod.capture(rule="all")
def all_candidate_windows(m) -> list[Window]:
    return filter_nonviable_windows(ui.windows())


@mod.capture(rule="gap")
def skip_window(m) -> list[Window]:
    return [Gap()]


@mod.capture(rule="<user.running_applications>")
def application_windows(m) -> list[Window]:
    return filter_nonviable_windows(
        [
            window
            for app in m.running_applications_list
            for window in actions.self.get_running_app(app).windows()
        ]
    )


@mod.capture(
    rule="<user.application_windows>|<user.numbered_windows>|<user.skip_window>"
)
def layout_item(m) -> list[Optional[Window]]:
    attributes = [
        "application_windows",
        "numbered_windows",
        "skip_window",
    ]
    num_passed = len(list(filter(lambda attrs: hasattr(m, attrs), attributes)))
    if num_passed > 1:
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
def numbered_windows(m) -> list[Window]:
    all_windows = filter_nonviable_windows(ui.windows())
    selected_windows = [
        all_windows[i - 1] for i in m.ordinals_small_list if i - 1 < len(all_windows)
    ]
    return selected_windows


@mod.capture(rule="<user.layout_item>+ [<user.all_candidate_windows>]")
def target_windows(m) -> list[Window]:
    windows = []
    if hasattr(m, "layout_item_list"):
        windows += [window for sublist in m.layout_item_list for window in sublist]

    if hasattr(m, "all_candidate_windows"):
        windows += [w for w in m.all_candidate_windows if w not in windows]
    return windows


def pick_split_arrangement(
    target_windows: Optional[list[Window]],
    layout_name: str,
) -> list[SnapPosition]:
    return SPLIT_POSITIONS[layout_name]


@mod.capture(rule="{user.window_split_positions} [<user.target_windows>]")
def window_layout(m) -> WindowLayout:
    global last_layout
    layout_name = m.window_split_positions
    window_was_specified = hasattr(m, "target_windows")

    target_windows = (
        m.target_windows
        if window_was_specified
        else filter_nonviable_windows(ui.windows())
    )

    layout = pick_split_arrangement(target_windows, layout_name)
    return WindowLayout(
        name=layout_name,
        split_positions=layout,
        windows=target_windows,
        can_rotate=True,
        rotation_count=0,
        finish_time=0,
    )


@mod.action_class
class Actions:
    def snap_layout(layout: WindowLayout):
        """Split the screen between multiple applications."""
        snap_layout(layout)


def focus_callback(_):
    global layout_in_progress
    global last_layout

    # Running a layout will generate focus events, which we don't consider to be manual
    # / user initiated, so skip in that case.
    if last_layout is None or layout_in_progress is not None:
        return

    # Track if the user has manually focused since layout and clear the state if so;
    # this way we won't rotate if that same layout request is made again.
    delta = time.perf_counter() - last_layout.finish_time
    if delta >= 1:
        last_layout = None


ui.register("app_activate", focus_callback)
ui.register("win_focus", focus_callback)
