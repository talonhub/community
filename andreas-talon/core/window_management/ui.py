from talon import Context, Module, ui, actions, ctrl
import time


mod = Module()
ctx = Context()


# @ctx.action_class("app")
# class AppActionsWin:
#     def window_previous():
#         cycle_windows(ui.active_app(), -1)

#     def window_next():
#         cycle_windows(ui.active_app(), 1)


@mod.action_class
class Actions:
    def get_app(name: str) -> ui.App:
        """Get application by name"""
        # Try to get application by name
        apps = [a for a in ui.apps(background=False) if a.name == name]

        # No application found for name
        if not apps:
            raise RuntimeError(f"App '{name}' not running")

        # Multiple hits on this application. Filter out invalid applications.
        if len(apps) > 1:
            apps2 = [a for a in apps if is_app_valid(a)]
            if apps2:
                return apps2[0]

        # Finally just pick the first application
        if apps:
            return apps[0]

    def get_app_window(app_name: str) -> ui.Window:
        """Get top window by application name"""
        app = actions.user.get_app(app_name)
        return app.windows()[0]

    def get_window_under_cursor() -> ui.Window:
        """Get the window under the mouse cursor"""
        x, y = ctrl.mouse_pos()
        windows = [
            w
            for w in ui.windows(hidden=False)
            if w.rect.contains(x, y) and is_window_valid(w) and is_app_valid(w.app)
        ]
        if not windows:
            raise Exception("Can't find window under the mouse cursor")
        return windows[0]

    def focus_app(app: ui.App):
        """Focus app and wait until finished"""
        app.focus()
        t1 = time.monotonic()
        while ui.active_app() != app:
            if time.monotonic() - t1 > 1:
                raise RuntimeError(f"Can't focus app: {app.name}")
            actions.sleep("50ms")

    def focus_window(window: ui.Window):
        """Focus window and wait until finished"""
        window.focus()

        t1 = time.monotonic()
        while ui.active_window() != window:
            if time.monotonic() - t1 > 1:
                raise RuntimeError(f"Can't focus window '{window.title}'")
            actions.sleep("50ms")

    def send_key(key: str, app: ui.App):
        """Send key <key> to application"""
        active_app = ui.active_app()
        if active_app != app:
            actions.user.focus_app(app)
            actions.key(key)
            actions.user.focus_app(active_app)
        else:
            actions.key(key)


def cycle_windows(app: ui.App, diff: int):
    active = app.active_window
    windows = [w for w in app.windows() if w == active or is_window_valid(w)]
    windows.sort(key=lambda w: w.id)
    current = windows.index(active)
    max = len(windows) - 1
    i = cycle(current + diff, 0, max)

    while i != current:
        try:
            actions.user.focus_window(windows[i])
            break
        except:
            i = cycle(i + diff, 0, max)


def is_app_valid(app: ui.App) -> bool:
    return (
        not app.background
        and not is_system_app(app)
        and is_window_valid(app.active_window)
    )


def is_window_valid(window: ui.Window) -> bool:
    return (
        not window.hidden
        and window.title != ""
        and window.rect.width > window.screen.dpi
        and window.rect.height > window.screen.dpi
    )


def is_system_app(app: ui.App):
    return app.exe.startswith("C:\\WINDOWS\\SystemApps") or app.exe.startswith(
        "C:\\WINDOWS\\system32"
    )


def cycle(value: int, min: int, max: int) -> int:
    """Cycle value between minimum and maximum"""
    if value < min:
        return max
    if value > max:
        return min
    return value
