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
        and window.title != ""
        # This excludes many tiny windows that are not actual windows, and is a rough heuristic.
        and window.rect.width > window.screen.dpi
        and window.rect.height > window.screen.dpi
    )
