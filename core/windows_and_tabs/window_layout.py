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
        actions.user.switcher_focus_window(window)

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


@mod.capture(
    rule="{user.window_split_positions} [<number_small>] [<user.target_windows>]"
)
def window_layout(m) -> WindowLayout:
    global last_focus_was_done_by_snap_layout
    if hasattr(m, "target_windows"):
        target_length = len(m.target_windows)
    else:
        target_length = len(_windows_under_active_window())
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
        target_windows = _windows_under_active_window()

    return WindowLayout(
        layout,
        target_windows,
        not hasattr(m, "target_windows") and last_focus_was_done_by_snap_layout,
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
