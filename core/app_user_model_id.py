"""Scope for the active window's AppUserModelIDs (Windows), for matching in .talon files:

    user.window_app_user_model_id: Microsoft.Windows.ControlPanel
    user.process_app_user_model_id: Microsoft.WindowsCalculator_8wekyb3d8bbwe!App

Both come from the shell's own resolver (see app_switcher/windows/app_resolver.py),
so they match what the taskbar uses:

window_app_user_model_id is the id the taskbar groups the window under. File Explorer
windows are Microsoft.Windows.Explorer, Control Panel windows (also explorer.exe)
Microsoft.Windows.ControlPanel, and Settings resolves to its own app even though its
frame belongs to ApplicationFrameHost.exe.

process_app_user_model_id is the id of the window's process as a whole: the same for
most apps, but the host for hosted windows (Microsoft.Windows.Explorer for Control
Panel, "{...}\\ApplicationFrameHost.exe" for Settings).

Apps with no id of their own get the shell's computed one, e.g.
"{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\cmd.exe". If the resolver isn't available,
the window value falls back to the id the window sets on itself and the process
value to a packaged app's id. Either is "" when unknown, and both are "" on other
platforms.
"""

from talon import Module, app, ui

mod = Module()

_values = {"window_app_user_model_id": "", "process_app_user_model_id": ""}
# Windows can set their id just after they get focus: Control Panel pages start out as
# Microsoft.Windows.Explorer and switch 0.1-0.3s later. Talon has no event for that, but
# the shell sends the taskbar a burst of HSHELL_REDRAW when it happens, so the ids are
# read again once a burst for the active window has been quiet this long.
SHELL_EVENT_DEBOUNCE_MS = 30
_hook = None


@mod.scope
def scope():
    return dict(_values)


if app.platform == "windows":
    import ctypes

    from .app_switcher.windows import app_resolver, shell_hook
    from .app_switcher.windows.app_identity import process_model_id, window_model_id, window_pid

    _user32 = ctypes.WinDLL("user32")
    _user32.GetForegroundWindow.restype = ctypes.c_void_p

    def _read(hwnd: int, pid: int) -> dict:
        window_id = app_resolver.window_app_id(hwnd)
        process_id = app_resolver.process_app_id(pid)
        if window_id is None and process_id is None and not app_resolver.available():
            window_id = window_model_id(hwnd)
            process_id = process_model_id(pid)
        return {
            "window_app_user_model_id": window_id or "",
            "process_app_user_model_id": process_id or "",
        }

    def _refresh_foreground(*_):
        # The foreground window as Windows sees it: Talon's active window can lag the
        # shell's notifications (a new Slack PWA window was seen 0.2s later).
        hwnd = _user32.GetForegroundWindow()
        if not hwnd:
            return
        try:
            values = _read(hwnd, window_pid(hwnd))
        except Exception as e:
            # e.g. the COM thread timing out; keep the last values.
            print(f"app_user_model_id: could not read ids: {e}")
            return
        if values != _values:
            _values.update(values)
            scope.update()

    def _on_shell_event(code: int, hwnd: int):
        # Called on the hook's thread; the deferred read runs there too.
        if code not in (
            shell_hook.HSHELL_REDRAW,
            shell_hook.HSHELL_WINDOWCREATED,
            shell_hook.HSHELL_WINDOWACTIVATED,
            shell_hook.HSHELL_RUDEAPPACTIVATED,
            shell_hook.HSHELL_WINDOWREPLACED,
        ):
            return
        if hwnd != _user32.GetForegroundWindow():
            return
        if _hook is None:  # a notification before start_shell_hook returned
            _refresh_foreground()
        else:
            _hook.after(SHELL_EVENT_DEBOUNCE_MS, _refresh_foreground)

    def _register():
        global _hook
        ui.register("win_focus", _refresh_foreground)
        _hook = shell_hook.start_shell_hook("app_user_model_id", _on_shell_event)
        if _hook is None:
            # Without the hook, fall back to Talon's title changes, which usually come
            # around the time a window sets its id.
            print("app_user_model_id: shell hook unavailable; using title changes")
            ui.register("win_title", _refresh_foreground)
        _refresh_foreground()

    app.register("ready", _register)
