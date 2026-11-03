"""ctypes wrappers for the Win32 and DWM calls the thumbnail switcher needs.

DWM thumbnails are composited by the desktop window manager straight onto a
destination window, so the egui window only has to reserve space for them; the
pixels never pass through Python.
"""

import ctypes
import os
import time
from ctypes import wintypes

from talon import app

from ..windows.window_filter import DWM_CLOAKED_SHELL, cloak_reason, is_alt_tab_window

DWM_TNP_RECTDESTINATION = 0x01
DWM_TNP_RECTSOURCE = 0x02
DWM_TNP_OPACITY = 0x04
DWM_TNP_VISIBLE = 0x08
DWM_TNP_SOURCECLIENTAREAONLY = 0x10

DWMWA_CLOAKED = 14
DWMWA_EXTENDED_FRAME_BOUNDS = 9

GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
WS_EX_NOACTIVATE = 0x08000000
WS_EX_TRANSPARENT = 0x00000020
RGN_DIFF = 4
GW_OWNER = 4
GA_ROOT = 2

SW_MAXIMIZE = 3
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
SW_SHOWNOACTIVATE = 4
SW_SHOWMINNOACTIVE = 7
SW_RESTORE = 9
WM_CLOSE = 0x0010
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
SWP_NOACTIVATE = 0x0010
WS_EX_LAYERED = 0x00080000
LWA_ALPHA = 0x2
MONITOR_DEFAULTTONEAREST = 2


class DWM_THUMBNAIL_PROPERTIES(ctypes.Structure):
    _fields_ = [
        ("dwFlags", wintypes.DWORD),
        ("rcDestination", wintypes.RECT),
        ("rcSource", wintypes.RECT),
        ("opacity", ctypes.c_ubyte),
        ("fVisible", wintypes.BOOL),
        ("fSourceClientAreaOnly", wintypes.BOOL),
    ]


class WINDOWPLACEMENT(ctypes.Structure):
    _fields_ = [
        ("length", wintypes.UINT),
        ("flags", wintypes.UINT),
        ("showCmd", wintypes.UINT),
        ("ptMinPosition", wintypes.POINT),
        ("ptMaxPosition", wintypes.POINT),
        ("rcNormalPosition", wintypes.RECT),
    ]


class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", wintypes.RECT),
        ("rcWork", wintypes.RECT),
        ("dwFlags", wintypes.DWORD),
    ]


if app.platform == "windows":
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    dwmapi = ctypes.WinDLL("dwmapi")

    HTHUMBNAIL = ctypes.c_void_p
    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    dwmapi.DwmRegisterThumbnail.argtypes = [
        wintypes.HWND,
        wintypes.HWND,
        ctypes.POINTER(HTHUMBNAIL),
    ]
    dwmapi.DwmRegisterThumbnail.restype = ctypes.c_long
    dwmapi.DwmUnregisterThumbnail.argtypes = [HTHUMBNAIL]
    dwmapi.DwmUnregisterThumbnail.restype = ctypes.c_long
    dwmapi.DwmUpdateThumbnailProperties.argtypes = [
        HTHUMBNAIL,
        ctypes.POINTER(DWM_THUMBNAIL_PROPERTIES),
    ]
    dwmapi.DwmUpdateThumbnailProperties.restype = ctypes.c_long
    dwmapi.DwmQueryThumbnailSourceSize.argtypes = [
        HTHUMBNAIL,
        ctypes.POINTER(wintypes.SIZE),
    ]
    dwmapi.DwmQueryThumbnailSourceSize.restype = ctypes.c_long
    dwmapi.DwmGetWindowAttribute.argtypes = [
        wintypes.HWND,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    dwmapi.DwmGetWindowAttribute.restype = ctypes.c_long

    user32.EnumWindows.argtypes = [WNDENUMPROC, wintypes.LPARAM]
    user32.GetWindowThreadProcessId.argtypes = [
        wintypes.HWND,
        ctypes.POINTER(wintypes.DWORD),
    ]
    user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.InternalGetWindowText.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.IsWindow.argtypes = [wintypes.HWND]
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.IsIconic.argtypes = [wintypes.HWND]
    user32.GetWindow.argtypes = [wintypes.HWND, wintypes.UINT]
    user32.GetWindow.restype = wintypes.HWND
    user32.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
    user32.GetAncestor.restype = wintypes.HWND
    user32.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.GetWindowLongW.restype = wintypes.LONG
    user32.SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.LONG]
    user32.SetWindowLongW.restype = wintypes.LONG
    user32.SetWindowRgn.argtypes = [wintypes.HWND, wintypes.HRGN, wintypes.BOOL]
    gdi32 = ctypes.WinDLL("gdi32")
    gdi32.CreateRectRgn.argtypes = [ctypes.c_int] * 4
    gdi32.CreateRectRgn.restype = wintypes.HRGN
    gdi32.CombineRgn.argtypes = [wintypes.HRGN, wintypes.HRGN, wintypes.HRGN, ctypes.c_int]
    gdi32.DeleteObject.argtypes = [wintypes.HANDLE]
    user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.PostMessageW.argtypes = [
        wintypes.HWND,
        wintypes.UINT,
        wintypes.WPARAM,
        wintypes.LPARAM,
    ]
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


def find_own_hwnd(title: str) -> int | None:
    """Find a top-level window of this (Talon) process with the given title.

    talon.egui.Window doesn't expose its native handle, so look it up by title.
    """
    pid = os.getpid()
    found = []
    buf = ctypes.create_unicode_buffer(256)

    def callback(hwnd, _lparam):
        owner = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
        if owner.value == pid:
            user32.GetWindowTextW(hwnd, buf, len(buf))
            if buf.value == title:
                found.append(hwnd)
                return False
        return True

    user32.EnumWindows(WNDENUMPROC(callback), 0)
    return found[0] if found else None


def process_image(hwnd: int) -> str:
    """The executable of the process that owns the window, or ""."""
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.QueryFullProcessImageNameW.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    ]
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    process = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, window_pid(hwnd))
    if not process:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(1024)
        size = wintypes.DWORD(len(buf))
        if not kernel32.QueryFullProcessImageNameW(process, 0, buf, ctypes.byref(size)):
            return ""
        return buf.value
    finally:
        kernel32.CloseHandle(process)


def window_class(hwnd: int) -> str:
    buf = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, buf, len(buf))
    return buf.value


def window_pid(hwnd: int) -> int:
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


def foreground() -> int | None:
    return user32.GetForegroundWindow() or None


def set_foreground(hwnd: int) -> bool:
    return bool(user32.SetForegroundWindow(hwnd))


def z_order() -> dict[int, int]:
    """Map every top-level hwnd to its z-order position (0 = topmost)."""
    order = {}

    def callback(hwnd, _lparam):
        order[hwnd] = len(order)
        return True

    user32.EnumWindows(WNDENUMPROC(callback), 0)
    return order


def is_cloaked(hwnd: int) -> bool:
    return cloak_reason(hwnd) != 0


def window_text(hwnd: int) -> str:
    """The window's title, read without messaging it, so a hung window can't block."""
    buf = ctypes.create_unicode_buffer(512)
    user32.InternalGetWindowText(hwnd, buf, len(buf))
    return buf.value


def is_minimized(hwnd: int) -> bool:
    return bool(user32.IsIconic(hwnd))


def restore(hwnd: int):
    user32.ShowWindow(hwnd, SW_RESTORE)


def minimize_quietly(hwnd: int):
    """Minimize without activating another window (which would close the switcher)."""
    user32.ShowWindow(hwnd, SW_SHOWMINNOACTIVE)


def restore_quietly(hwnd: int):
    """Restore a minimized window without activating it."""
    user32.ShowWindow(hwnd, SW_SHOWNOACTIVATE)


def is_maximized(hwnd: int) -> bool:
    return bool(user32.IsZoomed(hwnd))


def _wait_while(condition, timeout: float):
    end = time.monotonic() + timeout
    while condition() and time.monotonic() < end:
        time.sleep(0.01)


def unminimize(hwnd: int, timeout: float = 0.5):
    """Restore a minimized window without activating it, and wait until it is."""
    if is_minimized(hwnd):
        restore_quietly(hwnd)
        _wait_while(lambda: is_minimized(hwnd), timeout)


def make_normal(hwnd: int, timeout: float = 0.5):
    """Make a window neither minimized nor maximized, without activating it, so that
    it can be given a rect; a maximized window ignores one."""
    unminimize(hwnd, timeout)
    if is_maximized(hwnd):
        placement = WINDOWPLACEMENT()
        placement.length = ctypes.sizeof(placement)
        if user32.GetWindowPlacement(hwnd, ctypes.byref(placement)):
            placement.showCmd = SW_SHOWNOACTIVATE
            user32.SetWindowPlacement(hwnd, ctypes.byref(placement))
            _wait_while(lambda: is_maximized(hwnd), timeout)


def maximize(hwnd: int):
    user32.ShowWindow(hwnd, SW_MAXIMIZE)


def request_close(hwnd: int):
    """Ask a window to close, as its close button would; it may refuse or prompt."""
    user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)


def work_area(hwnd: int) -> tuple[int, int, int, int]:
    """The work area (left, top, right, bottom) of the monitor a window is on."""
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    monitor = user32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)
    user32.GetMonitorInfoW(monitor, ctypes.byref(mi))
    r = mi.rcWork
    return (r.left, r.top, r.right, r.bottom)


def foreground_work_area() -> tuple[int, int, int, int]:
    """The work area (left, top, right, bottom) of the monitor with the foreground window."""
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    monitor = user32.MonitorFromWindow(
        user32.GetForegroundWindow(), MONITOR_DEFAULTTONEAREST
    )
    user32.GetMonitorInfoW(monitor, ctypes.byref(mi))
    r = mi.rcWork
    return (r.left, r.top, r.right, r.bottom)


def make_overlay(hwnd: int, width: int, height: int, thickness: int):
    """Turn a window into a click-through, never-activated frame `thickness` wide.

    The window region keeps only the frame, so the inside shows (and clicks) through
    without needing a layered window.
    """
    style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_NOACTIVATE | WS_EX_TRANSPARENT)
    outer = gdi32.CreateRectRgn(0, 0, width, height)
    inner = gdi32.CreateRectRgn(thickness, thickness, width - thickness, height - thickness)
    gdi32.CombineRgn(outer, outer, inner, RGN_DIFF)
    gdi32.DeleteObject(inner)
    # The system owns the region from here on.
    user32.SetWindowRgn(hwnd, outer, True)


def make_scrim(hwnd: int, alpha: int):
    """Turn a window into a click-through, never-activated layer drawn at `alpha`
    (0-255) over whatever is below it."""
    style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_NOACTIVATE | WS_EX_TRANSPARENT)
    user32.SetLayeredWindowAttributes(wintypes.HWND(hwnd), 0, alpha, LWA_ALPHA)


def is_layered(hwnd: int) -> bool:
    return bool(user32.GetWindowLongW(hwnd, GWL_EXSTYLE) & WS_EX_LAYERED)


HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
WS_EX_TOPMOST = 0x00000008


def is_topmost(hwnd: int) -> bool:
    return bool(user32.GetWindowLongW(hwnd, GWL_EXSTYLE) & WS_EX_TOPMOST)


def raise_quietly(hwnd: int, topmost: bool | None = None):
    """Bring a window to the top of its band without activating it; with `topmost`
    False, out of the topmost band to the top of the ordinary windows.

    A plain SetWindowPos(HWND_TOP) "succeeds" but doesn't take an ordinary window
    above the active one (seen with Edge under a focused window); passing through
    the topmost band and back does, so ordinary windows go that way."""
    flags = SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
    if topmost is None and is_topmost(hwnd):
        # Always-on-top windows stay so.
        user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, flags)
        return
    user32.SetWindowPos(hwnd, wintypes.HWND(HWND_TOPMOST), 0, 0, 0, 0, flags)
    user32.SetWindowPos(hwnd, wintypes.HWND(HWND_NOTOPMOST), 0, 0, 0, 0, flags)


def place_below(hwnd: int, above: int):
    """Put `hwnd` directly below `above` in z-order (within the topmost band if
    `above` is topmost), without moving or activating it."""
    user32.SetWindowPos(hwnd, above, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)


def move_hwnd(hwnd: int, rect: tuple[int, int, int, int]):
    left, top, right, bottom = rect
    user32.SetWindowPos(
        hwnd, None, left, top, right - left, bottom - top, SWP_NOZORDER | SWP_NOACTIVATE
    )


def hwnd_rect(hwnd: int) -> tuple[int, int, int, int]:
    r = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    return (r.left, r.top, r.right, r.bottom)


def frame_rect(hwnd: int) -> tuple[int, int, int, int]:
    """The window's visible frame, without the invisible resize borders; the rect
    Talon's ui.Window.rect reads and sets."""
    r = wintypes.RECT()
    hr = dwmapi.DwmGetWindowAttribute(hwnd, DWMWA_EXTENDED_FRAME_BOUNDS, ctypes.byref(r), ctypes.sizeof(r))
    if hr != 0:
        return hwnd_rect(hwnd)
    return (r.left, r.top, r.right, r.bottom)


def placed_rect(hwnd: int) -> tuple[int, int, int, int]:
    """Where the window is, or for a minimized one where it comes back when restored
    (its current rect is off-screen then). The restored rect is in workspace
    coordinates, which differ from the screen's only by a taskbar on the top or left
    of the primary monitor: close enough to tell which screen it's on."""
    if is_minimized(hwnd):
        placement = WINDOWPLACEMENT()
        placement.length = ctypes.sizeof(placement)
        if user32.GetWindowPlacement(hwnd, ctypes.byref(placement)):
            r = placement.rcNormalPosition
            return (r.left, r.top, r.right, r.bottom)
    return hwnd_rect(hwnd)


def is_window(hwnd: int) -> bool:
    return bool(user32.IsWindow(hwnd))


def intersect(
    a: tuple[int, int, int, int], b: tuple[int, int, int, int]
) -> tuple[int, int, int, int] | None:
    left, top = max(a[0], b[0]), max(a[1], b[1])
    right, bottom = min(a[2], b[2]), min(a[3], b[3])
    return (left, top, right, bottom) if left < right and top < bottom else None


class Thumbnail:
    """One DWM thumbnail of `source` drawn into `destination`."""

    def __init__(self, destination: int, source: int):
        self.source = source
        self.handle = HTHUMBNAIL()
        hr = dwmapi.DwmRegisterThumbnail(destination, source, ctypes.byref(self.handle))
        if hr != 0:
            raise OSError(f"DwmRegisterThumbnail failed: 0x{hr & 0xFFFFFFFF:08x}")
        self.rect: tuple[int, int, int, int] | None = None
        # (destination, source) last sent to DWM, or None while hidden.
        self.state: tuple | None = None

    def source_size(self) -> tuple[int, int]:
        size = wintypes.SIZE()
        if dwmapi.DwmQueryThumbnailSourceSize(self.handle, ctypes.byref(size)) != 0:
            return (0, 0)
        return (size.cx, size.cy)

    def place(
        self,
        rect: tuple[int, int, int, int],
        clip: tuple[int, int, int, int] | None = None,
    ):
        """Show the thumbnail at `rect`, in physical pixels of the destination's client area.

        DWM draws thumbnails over everything in the destination window, so with `clip`
        only the part of the thumbnail inside it is shown: the destination is cut down
        to the visible part and the source is cropped to match.
        """
        src_w, src_h = self.source_size()
        visible = intersect(rect, clip) if clip is not None else rect
        if visible is None or src_w <= 0 or src_h <= 0:
            self.hide()
            return
        scale_x = src_w / max(rect[2] - rect[0], 1)
        scale_y = src_h / max(rect[3] - rect[1], 1)
        source = (
            round((visible[0] - rect[0]) * scale_x),
            round((visible[1] - rect[1]) * scale_y),
            round((visible[2] - rect[0]) * scale_x),
            round((visible[3] - rect[1]) * scale_y),
        )
        if (visible, source) == self.state:
            return
        props = DWM_THUMBNAIL_PROPERTIES()
        props.dwFlags = (
            DWM_TNP_RECTDESTINATION
            | DWM_TNP_RECTSOURCE
            | DWM_TNP_VISIBLE
            | DWM_TNP_OPACITY
            | DWM_TNP_SOURCECLIENTAREAONLY
        )
        props.rcDestination = wintypes.RECT(*visible)
        props.rcSource = wintypes.RECT(*source)
        props.opacity = 255
        props.fVisible = True
        props.fSourceClientAreaOnly = False
        if dwmapi.DwmUpdateThumbnailProperties(self.handle, ctypes.byref(props)) == 0:
            self.rect = visible
            self.state = (visible, source)

    def hide(self):
        if self.state is None:
            return
        props = DWM_THUMBNAIL_PROPERTIES()
        props.dwFlags = DWM_TNP_VISIBLE
        props.fVisible = False
        if dwmapi.DwmUpdateThumbnailProperties(self.handle, ctypes.byref(props)) == 0:
            self.rect = None
            self.state = None

    def close(self):
        if self.handle:
            dwmapi.DwmUnregisterThumbnail(self.handle)
            self.handle = HTHUMBNAIL()
