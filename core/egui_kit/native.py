"""Native window handling for egui windows: finding, moving and closing them.

talon.egui.Window doesn't expose its native handle, so windows are found by title
among this (Talon) process's top-level windows. Windows only; elsewhere these find
nothing and do nothing, so the kit still imports on macOS.
"""

import ctypes
import os
import sys

WINDOWS = sys.platform == "win32"

SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
SWP_NOACTIVATE = 0x0010
SWP_FRAMECHANGED = 0x0020
HWND_TOPMOST = -1
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
DWMWA_WINDOW_CORNER_PREFERENCE = 33
DWMWCP_ROUND = 2
MONITOR_DEFAULTTONEAREST = 2
WM_CLOSE = 0x0010

if WINDOWS:
    from ctypes import wintypes

    class MONITORINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("rcMonitor", wintypes.RECT),
            ("rcWork", wintypes.RECT),
            ("dwFlags", wintypes.DWORD),
        ]

    # Our own handle, so these argtypes never clash with another module's user32.
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows.argtypes = [WNDENUMPROC, wintypes.LPARAM]
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.IsWindow.argtypes = [wintypes.HWND]
    user32.GetForegroundWindow.restype = wintypes.HWND
    user32.SetForegroundWindow.argtypes = [wintypes.HWND]
    user32.SetWindowPos.argtypes = [
        wintypes.HWND,
        wintypes.HWND,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        wintypes.UINT,
    ]
    user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    user32.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
    user32.MonitorFromWindow.restype = wintypes.HMONITOR
    user32.GetMonitorInfoW.argtypes = [wintypes.HMONITOR, ctypes.POINTER(MONITORINFO)]
    user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    user32.GetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.GetWindowLongPtrW.restype = ctypes.c_ssize_t
    user32.SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
    user32.SetWindowLongPtrW.restype = ctypes.c_ssize_t


def own_windows(match) -> list[int]:
    """This process's top-level windows whose title passes `match(title)`."""
    if not WINDOWS:
        return []
    pid = os.getpid()
    found = []
    buf = ctypes.create_unicode_buffer(256)

    def callback(hwnd, _lparam):
        owner = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
        if owner.value == pid:
            user32.GetWindowTextW(hwnd, buf, len(buf))
            if match(buf.value):
                found.append(hwnd)
        return True

    user32.EnumWindows(WNDENUMPROC(callback), 0)
    return found


def find_own_hwnd(title: str) -> int | None:
    """A top-level window of this (Talon) process with exactly this title."""
    found = own_windows(lambda t: t == title)
    return found[0] if found else None


def close_own_windows(title_prefix: str) -> int:
    """Close (as the title bar's X would) this process's windows whose title starts with
    `title_prefix`, e.g. ones a previous load left behind. Returns how many."""
    found = own_windows(lambda t: t.startswith(title_prefix))
    for hwnd in found:
        user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
    return len(found)


def is_window(hwnd: int) -> bool:
    return WINDOWS and bool(user32.IsWindow(hwnd))


def foreground() -> int | None:
    return (user32.GetForegroundWindow() or None) if WINDOWS else None


def set_foreground(hwnd: int) -> bool:
    return WINDOWS and bool(user32.SetForegroundWindow(hwnd))


def move_hwnd(hwnd: int, rect: tuple[int, int, int, int]):
    """Move and size a window to (left, top, right, bottom), physical pixels."""
    if not WINDOWS:
        return
    left, top, right, bottom = rect
    user32.SetWindowPos(hwnd, None, left, top, right - left, bottom - top, SWP_NOZORDER | SWP_NOACTIVATE)


def raise_topmost(hwnd: int):
    """To the top of the topmost windows, without activating it."""
    if WINDOWS:
        user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)


def make_popup(hwnd: int):
    """Style a borderless window as a popup: off the taskbar and Alt+Tab (a tool
    window), with Windows 11's rounded corners."""
    if not WINDOWS:
        return
    ex = user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, (ex & ~WS_EX_APPWINDOW) | WS_EX_TOOLWINDOW)
    user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED)
    try:
        corner = ctypes.c_int(DWMWCP_ROUND)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(wintypes.HWND(hwnd), DWMWA_WINDOW_CORNER_PREFERENCE, ctypes.byref(corner), ctypes.sizeof(corner))
    except (AttributeError, OSError):
        pass  # before Windows 11


def hwnd_rect(hwnd: int) -> tuple[int, int, int, int]:
    if not WINDOWS:
        return (0, 0, 0, 0)
    r = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    return (r.left, r.top, r.right, r.bottom)


def _monitor_work_area(monitor) -> tuple[int, int, int, int]:
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    user32.GetMonitorInfoW(monitor, ctypes.byref(mi))
    r = mi.rcWork
    return (r.left, r.top, r.right, r.bottom)


def work_area(hwnd: int) -> tuple[int, int, int, int]:
    """The work area (left, top, right, bottom) of the monitor a window is on."""
    if not WINDOWS:
        return (0, 0, 0, 0)
    return _monitor_work_area(user32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST))


def foreground_work_area() -> tuple[int, int, int, int]:
    """The work area (left, top, right, bottom) of the monitor with the foreground window."""
    if not WINDOWS:
        return (0, 0, 0, 0)
    return _monitor_work_area(user32.MonitorFromWindow(user32.GetForegroundWindow(), MONITOR_DEFAULTTONEAREST))
