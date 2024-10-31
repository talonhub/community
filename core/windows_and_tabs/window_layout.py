import copy
from dataclasses import dataclass
from datetime import datetime

"""Tools for laying out windows in an arrangement """

import logging
from typing import Any, Dict, Optional

from talon import Context, Module, actions, settings, ui

mod = Module()

mod.list(
    "window_split_positions",
    "Predefined window positions when splitting the screen between multiple windows.",
)

last_focus_was_done_by_snap_layout = False
lay_out_start_time = datetime.now()


def _focus_callback(_):
    global last_focus_was_done_by_snap_layout
    global lay_out_start_time

    if (datetime.now() - lay_out_start_time).total_seconds() >= 1:
        print("Resetting last focus")
        last_focus_was_done_by_snap_layout = False


@dataclass
class WindowLayout:
    """Represents a layout of windows on a screen"""

    layout: list[str]
    windows: list[Any]
    should_rotate: bool


_split_positions = {
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


def _snap_next(windows: list[Any], target_layout: str) -> Optional[int]:
    for index, window in enumerate(windows):
        if window is None:
            return index
        try:
            actions.user.snap_target_window_to_position(
                window,
                target_layout,
            )
            return index
        except Exception as e:
            print(
                f"Failed to snap window for application (this is normal) {window.app.name} {window.title}: {e}"
            )
    return None


def _snap_layout(window_layout: WindowLayout):
    """Split the screen between multiple windows."""
    global last_focus_was_done_by_snap_layout
    global lay_out_start_time

    lay_out_start_time = datetime.now()

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
        try:
            actions.user.switcher_focus_window(window)
        except Exception as ex:
            print(
                f"Failed to focus window for application {window.app.name} {window.title}: {ex}"
            )

    last_focus_was_done_by_snap_layout = True


def _windows_under_active_window() -> list[Any]:
    active_window = ui.active_window()
    ui_windows = ui.windows()
    try:
        active_index = ui_windows.index(active_window)
        return ui_windows[active_index:]
    except Exception:
        return ui_windows


@mod.capture(rule="all")
def all_candidate_windows(m) -> list[Any]:
    return _windows_under_active_window()


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
    all_windows = _windows_under_active_window()
    selected_windows = [
        all_windows[i - 1] for i in m.ordinals_small_list if i - 1 < len(all_windows)
    ]
    return selected_windows


@mod.capture(rule="<user.layout_item>+ [<user.all_candidate_windows>]")
def target_windows(m) -> list[Any]:
    windows = []
    if hasattr(m, "layout_item_list"):
        windows += [window for sublist in m.layout_item_list for window in sublist]

    if hasattr(m, "all_candidate_windows"):
        windows += [w for w in m.all_candidate_windows if w not in windows]
    return windows


def _pick_split_arrangement(
    target_windows, window_split_positions, number_small
) -> list[str]:
    if target_windows is not None:
        target_length = len(target_windows)
    else:
        target_length = len(_windows_under_active_window())
    if number_small is not None:
        return _split_positions[window_split_positions][number_small]
    else:
        closest_key = min(
            _split_positions[window_split_positions].keys(),
            key=lambda k: abs(k - target_length),
        )
        return _split_positions[window_split_positions][closest_key]


@mod.capture(
    rule="{user.window_split_positions} [<number_small>] [<user.target_windows>]"
)
def window_layout(m) -> WindowLayout:
    global last_focus_was_done_by_snap_layout
    window_was_specified = hasattr(m, "target_windows")
    specified_layout_count = m.number_small if hasattr(m, "number_small") else None
    target_windows = (
        m.target_windows if window_was_specified else _windows_under_active_window()
    )

    layout = _pick_split_arrangement(
        target_windows, m.window_split_positions, specified_layout_count
    )

    return WindowLayout(
        layout,
        target_windows,
        not window_was_specified and last_focus_was_done_by_snap_layout,
    )


ctx = Context()

ctx.lists["user.window_split_positions"] = _split_positions.keys()


@mod.action_class
class Actions:
    def snap_layout(
        window_layout: WindowLayout,
    ):
        """Split the screen between multiple applications."""
        _snap_layout(window_layout)


ui.register("app_activate", _focus_callback)
ui.register("win_focus", _focus_callback)
