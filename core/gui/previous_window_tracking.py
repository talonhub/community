# this is provided as a temporary workaround for being able to focus the previous window after closing an egui

from dataclasses import dataclass

from talon import app, ui


@dataclass
class WindowTrackingState:
    current_window: ui.Window = None
    previous_window: ui.Window = None


window_tracking_state = WindowTrackingState()


def focus_callback(window):
    if not window or window == window_tracking_state.current_window:
        return
    window_tracking_state.previous_window = window_tracking_state.current_window
    window_tracking_state.current_window = window


def activate_callback(application):
    if application.active_window:
        focus_callback(application.active_window)


ui.register("win_focus", focus_callback)
ui.register("app_activate", activate_callback)


def get_current_window():
    return window_tracking_state.current_window


def get_previous_window():
    return window_tracking_state.previous_window


def on_ready():
    window_tracking_state.current_window = ui.active_window()


app.register("ready", on_ready)
