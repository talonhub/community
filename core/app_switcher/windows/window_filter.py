"""Which windows count as switchable apps: roughly the rule Alt+Tab and the taskbar use.

Shared by the app switcher (the running list) and the thumbnail switcher. Minimized
windows count; windows DWM hides (cloaks) don't, except those parked on another virtual
desktop. Size heuristics don't work here: a minimized window reports a tiny rect, while
hidden system windows (TextInputHost, SearchHost) can be screen-sized.
"""

import ctypes
import time
from ctypes import wintypes

from talon import app

from . import virtual_desktops as vd

DWMWA_CLOAKED = 14
# Cloaked by the shell: windows on other virtual desktops, but also hidden system UI
# (Search, the touch keyboard host) and suspended UWP apps.
DWM_CLOAKED_SHELL = 2

GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
WS_EX_NOACTIVATE = 0x08000000
GW_OWNER = 4
GA_ROOT = 2
# How long the answer to "is this hidden window on another desktop?" is kept.
DESKTOP_CHECK_SECONDS = 2.0
# hwnd -> (when asked, on another desktop)
_on_other_desktop: dict[int, tuple[float, bool]] = {}

if app.platform == "windows":
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    dwmapi = ctypes.WinDLL("dwmapi")
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.GetWindow.argtypes = [wintypes.HWND, wintypes.UINT]
    user32.GetWindow.restype = wintypes.HWND
    user32.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
    user32.GetAncestor.restype = wintypes.HWND
    user32.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.GetWindowLongW.restype = wintypes.LONG
    dwmapi.DwmGetWindowAttribute.argtypes = [wintypes.HWND, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD]
    dwmapi.DwmGetWindowAttribute.restype = ctypes.c_long


def cloak_reason(hwnd: int) -> int:
    """Why DWM hides the window, 0 if it doesn't: suspended UWP apps, other virtual
    desktops and hidden shell UI (DWM_CLOAKED_SHELL), ..."""
    cloaked = wintypes.DWORD()
    hr = dwmapi.DwmGetWindowAttribute(hwnd, DWMWA_CLOAKED, ctypes.byref(cloaked), ctypes.sizeof(cloaked))
    return cloaked.value if hr == 0 else 0


def is_alt_tab_window(hwnd: int, shell_cloaked_ok: bool = False) -> bool:
    """Roughly the rule Alt+Tab uses to decide whether a window gets an entry.

    Minimized windows pass: they are still visible in the Win32 sense. With
    `shell_cloaked_ok`, so do windows the shell cloaked, like those on other virtual
    desktops; the caller checks which those are (see is_switchable).
    """
    if not user32.IsWindowVisible(hwnd):
        return False
    reason = cloak_reason(hwnd)
    if reason and not (shell_cloaked_ok and reason == DWM_CLOAKED_SHELL):
        return False
    # Talon also lists some child windows, e.g. Chromium's render widgets.
    if user32.GetAncestor(hwnd, GA_ROOT) != hwnd:
        return False
    ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    if ex_style & WS_EX_APPWINDOW:
        return True
    if ex_style & (WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE):
        return False
    return not user32.GetWindow(hwnd, GW_OWNER)


def is_switchable(hwnd: int) -> bool:
    """Whether a window is an app window to switch to, on this desktop or another one."""
    if not is_alt_tab_window(hwnd, shell_cloaked_ok=True):
        return False
    if cloak_reason(hwnd) != DWM_CLOAKED_SHELL:
        return True
    # Shell-cloaked: only windows parked on another virtual desktop. Asking takes a
    # trip to the COM thread, and the running list asks for every such window on each
    # app event, so the answer is kept for a moment.
    now = time.monotonic()
    cached = _on_other_desktop.get(hwnd)
    if cached is not None and now - cached[0] < DESKTOP_CHECK_SECONDS:
        return cached[1]
    try:
        away = vd.window_desktop(hwnd) is not None and not vd.is_on_current_desktop(hwnd)
    except OSError:
        away = False
    if len(_on_other_desktop) > 500:
        _on_other_desktop.clear()
    _on_other_desktop[hwnd] = (now, away)
    return away


if app.platform == "windows":
    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows.argtypes = [WNDENUMPROC, wintypes.LPARAM]


def z_order() -> dict[int, int]:
    """Every top-level window's place in the z-order (0 = topmost): the most recently
    used window of an app comes first."""
    order = {}

    def callback(hwnd, _lparam):
        order[hwnd] = len(order)
        return True

    user32.EnumWindows(WNDENUMPROC(callback), 0)
    return order
