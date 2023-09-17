from talon import Context, actions, ui

ctx = Context()


@ctx.action_class("app")
class AppActions:
    def window_previous():
        cycle_windows(ui.active_app(), -1)

    def window_next():
        cycle_windows(ui.active_app(), 1)


def cycle_windows(app: ui.App, diff: int):
    """Cycle windows backwards or forwards for the given application"""
    active = app.active_window
    windows = [w for w in app.windows() if w == active or is_window_valid(w)]
    windows.sort(key=lambda w: w.id)
    current = windows.index(active)
    max = len(windows) - 1
    i = cycle(current + diff, 0, max)

    while i != current:
        try:
            actions.user.switcher_focus_window(windows[i])
            break
        except Exception:
            i = cycle(i + diff, 0, max)


def is_window_valid(window: ui.Window) -> bool:
    """Returns true if this window is valid for focusing"""
    return (
        not window.hidden
        and window.title != ""
        and window.rect.width > window.screen.dpi
        and window.rect.height > window.screen.dpi
    )


def cycle(value: int, min: int, max: int) -> int:
    """Cycle value between minimum and maximum"""
    if value < min:
        return max
    if value > max:
        return min
    return value
