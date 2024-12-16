from talon import Context, actions, ui

ctx = Context()


@ctx.action_class("app")
class AppActions:
    def window_previous():
        cycle_windows(ui.active_app(), -1)

    def window_next():
        cycle_windows(ui.active_app(), 1)

def get_valid_windows(app: ui.App):
    valid_windows = []
    for window in app.windows():
        if is_window_valid(window):
            valid_windows.append(window)

    return valid_windows

def cycle_windows(app: ui.App, diff: int):
    """Cycle windows backwards or forwards for the given application"""
    active = app.active_window
    windows = get_valid_windows(app)
    windows.sort(key=lambda w: w.id)
    current = windows.index(active)
    i = (current + diff) % len(windows)

    while i != current:
        try:
            actions.user.switcher_focus_window(windows[i])
            break
        except Exception:
            i = (i + diff) % len(windows)


def is_window_valid(window: ui.Window) -> bool:
    """Returns true if this window is valid for focusing"""
    return (
        not window.hidden
        # On Windows, there are many fake windows with empty titles -- this excludes them.
        and len(window.title) > 0
        # This excludes many tiny windows that are not actual windows, and is a rough heuristic.
        and window.rect.width > window.screen.dpi
        and window.rect.height > window.screen.dpi
    )