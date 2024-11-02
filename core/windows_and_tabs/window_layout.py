import copy
from dataclasses import dataclass
from typing import List, Optional, Union
from time import perf_counter

from talon import Context, Module, actions, settings, ui

"""Tools for laying out windows in an arrangement """

from talon import Context, Module, actions, settings
from talon.ui import Window, UIErr

mod = Module()

mod.list(
    "window_split_positions",
    "Predefined window positions when splitting the screen between multiple windows.",
)


def focus_callback(_):
    global layout_in_progress
    global last_layout
    if layout_in_progress is not None:
        return

    delta = 1
    if last_layout is not None:
        delta = perf_counter() - last_layout.finish_time
    print(f"delta ispr{delta}")
    if delta >= 1:
        print("Resetting last focus")
        last_layout = None


@dataclass
class WindowLayout:
    """Represents a layout of windows on a screen"""

    layout: list[str]
    windows: list[Window]
    should_rotate: bool
    finish_time: float


layout_in_progress: Optional[WindowLayout] = None
last_layout: Optional[WindowLayout] = None


SPLIT_POSITIONS = {
    "split": {
        2: ["left", "right"],
        3: [
            "left third",
            "center third",
            "right third",
        ],
    },
    "clock": {
        3: [
            "left",
            "top right",
            "bottom right",
        ],
    },
    "counterclock": {
        3: [
            "right",
            "top left",
            "bottom left",
        ],
    },
}


def snap_next(windows: list[Window], target_layout: str) -> Optional[int]:
    for idx, window in enumerate(windows):
        if window is None:
            return idx
        try:
            actions.user.snap_target_window_to_position(
                window,
                target_layout,
            )

            return idx
        except UIErr as e:
            print(
                f'Failed to snap {window.app.name}\'s "{window.title}" window ({type(e).__name__} {e});  this is normal; continuing to the next'
            )
    return None


def snap_layout(window_layout: WindowLayout):
    """Split the screen between multiple windows."""
    global layout_in_progress
    global last_layout

    layout_in_progress = window_layout
    target_layout = copy.deepcopy(window_layout.layout)
    remaining_windows = window_layout.windows
    snapped_windows = []
    snapped_window_idx = 0
    if window_layout.should_rotate:
        print("Trying to rotate")
        target_layout.append(target_layout.pop(0))

    while len(target_layout) > 0:
        snapped_window_idx = snap_next(remaining_windows, target_layout.pop(0))
        if snapped_window_idx is not None:
            snapped_windows.insert(0, remaining_windows[snapped_window_idx])
            remaining_windows = remaining_windows[snapped_window_idx + 1 :]

    if window_layout.should_rotate and len(snapped_windows) > 0:
        snapped_windows.append(snapped_windows.pop(0))

    for window in snapped_windows:
        try:
            actions.user.switcher_focus_window(window)
        except Exception as ex:
            print(
                f"Failed to focus window for application {window.app.name} {window.title}: {ex}"
            )

    layout_in_progress.finish_time = perf_counter()
    last_layout = layout_in_progress
    layout_in_progress = None


def filter_nonviable_windows(windows: List[Window]) -> list[Window]:
    active_window = ui.active_window()

    # Many invisible non-resizable windows are identifiable because they exist above the current window
    # in the z-index
    active_window_idx = windows.index(active_window)  # type: ignore
    return list(filter(lambda w: windows.index(w) >= active_window_idx, windows))


@mod.capture(rule="all")
def all_candidate_windows(m) -> list[Window]:
    return filter_nonviable_windows(ui.windows())


@mod.capture(rule="gap")
def skip_window(m) -> list[Window]:
    return [None]


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
    target_windows, window_split_positions, number_small
) -> list[str]:
    if target_windows is not None:
        target_length = len(target_windows)
    else:
        target_length = len(filter_nonviable_windows(ui.windows()))
    if number_small is not None:
        return SPLIT_POSITIONS[window_split_positions][number_small]
    else:
        closest_key = min(
            SPLIT_POSITIONS[window_split_positions].keys(),
            key=lambda k: abs(k - target_length),
        )
        return SPLIT_POSITIONS[window_split_positions][closest_key]


@mod.capture(
    rule="{user.window_split_positions} [<number_small>] [<user.target_windows>]"
)
def window_layout(m) -> WindowLayout:
    global last_focus_was_done_by_snap_layout
    window_was_specified = hasattr(m, "target_windows")
    specified_layout_count = m.number_small if hasattr(m, "number_small") else None
    target_windows = (
        m.target_windows
        if window_was_specified
        else filter_nonviable_windows(ui.windows())
    )
    print(f"target windows is {target_windows}")

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


ctx = Context()

ctx.lists["user.window_split_positions"] = SPLIT_POSITIONS.keys()


@mod.action_class
class Actions:
    def snap_layout(
        window_layout: WindowLayout,
    ):
        """Split the screen between multiple applications."""
        snap_layout(window_layout)


ui.register("app_activate", focus_callback)
ui.register("win_focus", focus_callback)
