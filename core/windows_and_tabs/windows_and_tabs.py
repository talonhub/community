from talon import Context, Module, actions, ui

mod = Module()
ctx = Context()


@ctx.action_class("app")
class AppActions:
    def window_previous():
        cycle_windows(ui.active_app(), -1)

    def window_next():
        cycle_windows(ui.active_app(), 1)


@mod.action_class
class Actions:
    def window_maximize():
        """Maximize the current window"""

    def window_reopen():
        """Reopen the last-closed window"""

    def window_restore():
        """Restore (unmaximize) the current window"""


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
    try:
        return (
            not window.hidden
            # On Windows, there are many fake windows with empty titles -- this excludes them.
            and len(window.title) > 0
            and (window.title not in ("Chrome Legacy Window"))
            # This excludes many tiny windows that are not actual windows, and is a rough heuristic.
            and window.rect.width > window.screen.dpi
            and window.rect.height > window.screen.dpi
        )
    except AttributeError:
        # Handle case where window.rect might not be accessible
        return False
