import copy
from dataclasses import dataclass
from time import perf_counter
from typing import List, Optional, Union

from talon import Context, Module, actions, settings, ui

"""Tools for laying out windows in an arrangement """

from talon import Context, Module, actions, settings
from talon.ui import UIErr, Window

SPLIT_POSITIONS = {
    "split": {
        2: ["Left", "Right"],
        3: [
            "LeftThird",
            "CenterThird",
            "RightThird",
        ],
    },
    "clock": {
        3: [
            "Left",
            "TopRight",
            "BottomRight",
        ],
    },
    "counterclock": {
        3: [
            "Right",
            "TopLeft",
            "BottomLeft",
        ],
    },
}

mod = Module()

mod.list(
    "window_split_positions",
    "Predefined window positions when splitting the screen between multiple windows.",
)
ctx = Context()

ctx.lists["user.window_split_positions"] = SPLIT_POSITIONS.keys()


def focus_callback(_):
    global layout_in_progress
    global last_layout
    if layout_in_progress is not None:
        return

    delta = 1
    if last_layout is not None:
        delta = perf_counter() - last_layout.finish_time
    if delta >= 1:
        last_layout = None


@dataclass
class WindowLayout:
    """Represents a layout of windows on a screen"""

    split_positions: list[str]
    windows: list[Window]
    should_rotate: bool
    finish_time: float


class GapWindow:
    pass


layout_in_progress: Optional[WindowLayout] = None
last_layout: Optional[WindowLayout] = None


def snap_next(windows: list[Window], target_layout: str) -> Optional[Window]:
    """This function snaps a window and returns the window if successful"""
    while windows:
        window = windows.pop(0)
        if isinstance(window, GapWindow):
            return window
        try:
            actions.user.snap_window_to_position(
                target_layout,
                window,
            )

            return window
        except (UIErr, AttributeError) as e:
            print(
                f'Failed to snap {window.app.name}\'s "{window.title}" window ({type(e).__name__} {e});  this is normal; continuing to the next'
            )
    return GapWindow()


def snap_layout(layout_config: WindowLayout):
    try:
        """Split the screen between multiple windows."""
        global layout_in_progress, last_layout

        layout_in_progress = layout_config
        remaining_windows = layout_config.windows
        print(f"Trying to snap these windows:{remaining_windows}")

        snapped_windows = []
        if layout_config.should_rotate:
            layout_config.split_positions.append(layout_config.split_positions.pop(0))

        while len(layout_config.split_positions) > 0:
            snapped_window: Window = snap_next(
                remaining_windows, layout_config.split_positions.pop(0)
            )
            snapped_windows.insert(0, snapped_window)

        if layout_config.should_rotate and len(snapped_windows) > 0:
            snapped_windows.append(snapped_windows.pop(0))

        for window in snapped_windows:
            if isinstance(window, GapWindow):
                continue
            actions.user.switcher_focus_window(window)

        layout_in_progress.finish_time = perf_counter()
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
            lambda w: all_windows.index(w) >= active_window_idx,
            windows,
        )
    )


@mod.capture(rule="all")
def all_candidate_windows(m) -> list[Window]:
    return filter_nonviable_windows(ui.windows())


@mod.capture(rule="gap")
def skip_window(m) -> list[Window]:
    return [GapWindow()]


@mod.capture(rule="<user.running_applications>")
def application_windows(m) -> list[Window]:
    return [
        window
        for app in m.running_applications_list
        for window in actions.self.get_running_app(app).windows()
    ]


@mod.capture(
    rule="<user.application_windows>|<user.numbered_windows>|<user.skip_window>"
)
def layout_item(m) -> list[Union[Window, None]]:
    # Check for multiple attributes and raise an error if found

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
    target_windows: Union[list[Window], None],
    window_split_positions: str,
    number_small: Union[int, None],
) -> list[str]:
    if target_windows is not None:
        target_length = len(target_windows)
    else:
        target_length = len(filter_nonviable_windows(ui.windows()))
    if number_small is not None:
        return copy.deepcopy(SPLIT_POSITIONS[window_split_positions][number_small])
    else:
        closest_key = min(
            SPLIT_POSITIONS[window_split_positions].keys(),
            key=lambda k: abs(k - target_length),
        )
        return copy.deepcopy(SPLIT_POSITIONS[window_split_positions][closest_key])


@mod.capture(
    rule="{user.window_split_positions} [<number_small>] [<user.target_windows>]"
)
def window_layout(m) -> WindowLayout:
    global last_layout
    window_was_specified = hasattr(m, "target_windows")
    specified_layout_count = m.number_small if hasattr(m, "number_small") else None
    target_windows = (
        m.target_windows
        if window_was_specified
        else filter_nonviable_windows(ui.windows())
    )

    layout = pick_split_arrangement(
        target_windows, m.window_split_positions, specified_layout_count
    )

    return WindowLayout(
        layout,
        target_windows,
        not window_was_specified
        and last_layout is not None
        and perf_counter() - last_layout.finish_time > 1,
        0,
    )


@mod.action_class
class Actions:
    def snap_layout(
        window_layout: WindowLayout,
    ):
        """Split the screen between multiple applications."""
        snap_layout(window_layout)


ui.register("app_activate", focus_callback)
ui.register("win_focus", focus_callback)
