"""Shell hook notifications: the messages the taskbar gets about top-level windows.

RegisterShellHookWindow sends a window the HSHELL_* notifications the taskbar uses to
add, activate and refresh its buttons. Notably HSHELL_REDRAW arrives in a burst when a
window sets its AppUserModelID (and when its title changes), which Talon has no event
for: Control Panel windows start out as Microsoft.Windows.Explorer and switch to
Microsoft.Windows.ControlPanel a moment later, and the taskbar re-resolves on these.

Each hook runs a hidden message-only window on a thread of its own. Callbacks are
called on that thread with (code, hwnd). Work can be deferred with ShellHook.after,
which also runs on that thread: cron.after from this thread was measured firing
0.2-1s late, too slow to follow these bursts.
"""

import ctypes
import sys
import threading
from ctypes import wintypes

from talon import app

HSHELL_WINDOWCREATED = 1
HSHELL_WINDOWDESTROYED = 2
HSHELL_WINDOWACTIVATED = 4
HSHELL_REDRAW = 6
HSHELL_WINDOWREPLACED = 13
# HSHELL_WINDOWACTIVATED with the 0x8000 flag set (a full-screen app is running).
HSHELL_RUDEAPPACTIVATED = 0x8004

WM_DESTROY = 0x0002
WM_CLOSE = 0x0010
WM_TIMER = 0x0113
_TIMER_ID = 1
HWND_MESSAGE = -3

# Hooks by name, kept on sys so a hot reload stops the previous module's hook.
_STASH = "_talon_shell_hooks"

if app.platform == "windows":
    _user32 = ctypes.WinDLL("user32", use_last_error=True)
    _kernel32 = ctypes.WinDLL("kernel32")
    _WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

    class _WNDCLASSW(ctypes.Structure):
        _fields_ = [
            ("style", wintypes.UINT),
            ("lpfnWndProc", _WNDPROC),
            ("cbClsExtra", ctypes.c_int),
            ("cbWndExtra", ctypes.c_int),
            ("hInstance", wintypes.HINSTANCE),
            ("hIcon", wintypes.HICON),
            ("hCursor", wintypes.HANDLE),
            ("hbrBackground", wintypes.HBRUSH),
            ("lpszMenuName", wintypes.LPCWSTR),
            ("lpszClassName", wintypes.LPCWSTR),
        ]

    _user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    _user32.DefWindowProcW.restype = ctypes.c_ssize_t
    _user32.RegisterClassW.argtypes = [ctypes.POINTER(_WNDCLASSW)]
    _user32.RegisterClassW.restype = wintypes.ATOM
    _user32.UnregisterClassW.argtypes = [wintypes.LPCWSTR, wintypes.HINSTANCE]
    _user32.CreateWindowExW.argtypes = [
        wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD,
        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
        wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID,
    ]
    _user32.CreateWindowExW.restype = wintypes.HWND
    _user32.RegisterShellHookWindow.argtypes = [wintypes.HWND]
    _user32.DeregisterShellHookWindow.argtypes = [wintypes.HWND]
    _user32.RegisterWindowMessageW.argtypes = [wintypes.LPCWSTR]
    _user32.RegisterWindowMessageW.restype = wintypes.UINT
    _user32.GetMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
    _user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    _user32.SetTimer.argtypes = [wintypes.HWND, ctypes.c_size_t, wintypes.UINT, ctypes.c_void_p]
    _user32.SetTimer.restype = ctypes.c_size_t
    _user32.KillTimer.argtypes = [wintypes.HWND, ctypes.c_size_t]
    _kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
    _kernel32.GetModuleHandleW.restype = wintypes.HMODULE


class ShellHook:
    def __init__(self, name: str, callback):
        self.name = name
        self.callback = callback
        self.hwnd = None
        self._shellhook_message = _user32.RegisterWindowMessageW("SHELLHOOK")
        # Unique per hook: a class registered by an older, reloaded module would keep
        # pointing at that module's window procedure.
        self._class_name = f"TalonShellHook_{name}_{id(self):x}"
        self._wndproc = _WNDPROC(self._window_proc)  # kept alive while the window lives
        self._pending = None  # the function ShellHook.after will run
        self._ready = threading.Event()
        self._thread = threading.Thread(target=self._run, name=f"shell hook ({name})", daemon=True)
        self._thread.start()
        self._ready.wait(5)

    def _window_proc(self, hwnd, msg, wparam, lparam):
        if msg == self._shellhook_message:
            try:
                self.callback(wparam, lparam)
            except Exception as e:
                print(f"shell hook ({self.name}): callback failed: {e}")
            return 0
        if msg == WM_TIMER and wparam == _TIMER_ID:
            _user32.KillTimer(hwnd, _TIMER_ID)
            fn, self._pending = self._pending, None
            if fn is not None:
                try:
                    fn()
                except Exception as e:
                    print(f"shell hook ({self.name}): deferred call failed: {e}")
            return 0
        if msg == WM_DESTROY:
            _user32.DeregisterShellHookWindow(hwnd)
            _user32.PostQuitMessage(0)
            return 0
        return _user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def _run(self):
        instance = _kernel32.GetModuleHandleW(None)
        window_class = _WNDCLASSW()
        window_class.lpfnWndProc = self._wndproc
        window_class.hInstance = instance
        window_class.lpszClassName = self._class_name
        try:
            if not _user32.RegisterClassW(ctypes.byref(window_class)):
                print(f"shell hook ({self.name}): RegisterClassW failed: {ctypes.get_last_error()}")
                return
            # A message-only window: never shown, and not in window lists.
            self.hwnd = _user32.CreateWindowExW(
                0, self._class_name, self._class_name, 0, 0, 0, 0, 0,
                wintypes.HWND(HWND_MESSAGE), None, instance, None,
            )
            if not self.hwnd or not _user32.RegisterShellHookWindow(self.hwnd):
                print(f"shell hook ({self.name}): could not register: {ctypes.get_last_error()}")
                return
        finally:
            self._ready.set()
        msg = wintypes.MSG()
        while _user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            _user32.TranslateMessage(ctypes.byref(msg))
            _user32.DispatchMessageW(ctypes.byref(msg))
        _user32.UnregisterClassW(self._class_name, instance)

    def after(self, milliseconds: int, fn):
        """Run fn on the hook's thread after `milliseconds`, replacing any call still
        pending, so a burst of notifications runs it once, after the burst. Call from
        the hook's thread (i.e. from the callback)."""
        self._pending = fn
        # Re-arming the same timer id restarts its countdown.
        _user32.SetTimer(self.hwnd, _TIMER_ID, milliseconds, None)

    def stop(self):
        if self.hwnd:
            # The window is destroyed on its own thread, which then leaves its loop.
            _user32.PostMessageW(self.hwnd, WM_CLOSE, 0, 0)

    @property
    def running(self) -> bool:
        return self.hwnd is not None and self._thread.is_alive()


def start_shell_hook(name: str, callback) -> "ShellHook | None":
    """Start a hook calling callback(code, hwnd) for every HSHELL_* notification, on the
    hook's own thread. A hook of the same name (from before a hot reload) is stopped."""
    if app.platform != "windows":
        return None
    hooks = getattr(sys, _STASH, None)
    if hooks is None:
        hooks = {}
        setattr(sys, _STASH, hooks)
    old = hooks.pop(name, None)
    if old is not None:
        old.stop()
    hook = ShellHook(name, callback)
    if not hook.running:
        return None
    hooks[name] = hook
    return hook
