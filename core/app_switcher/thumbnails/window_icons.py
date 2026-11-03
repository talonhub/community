"""Window icons as RGBA pixels, for tiles whose DWM thumbnail would be blank (minimized).

Large icons come from the shell (IShellItemImageFactory) for the app's AppUserModelID
or executable; the window's own HICON (WM_GETICON, then the class icon) is the fallback.
"""

import ctypes
import os
import re
from ctypes import wintypes

from talon import app

from ..windows import shell_apps, shell_com
from ..windows.com_thread import on_com_thread
from ..windows.shell_com import GUID

ICON_SIZE = 128

WM_GETICON = 0x007F
ICON_SMALL = 0
ICON_BIG = 1
ICON_SMALL2 = 2
SMTO_ABORTIFHUNG = 0x0002
GCLP_HICON = -14
GCLP_HICONSM = -34

SIIGBF_BIGGERSIZEOK = 0x01
SIIGBF_ICONONLY = 0x04
SIIGBF_THUMBNAILONLY = 0x08
BI_RGB = 0
DIB_RGB_COLORS = 0


class BITMAP(ctypes.Structure):
    _fields_ = [
        ("bmType", wintypes.LONG),
        ("bmWidth", wintypes.LONG),
        ("bmHeight", wintypes.LONG),
        ("bmWidthBytes", wintypes.LONG),
        ("bmPlanes", wintypes.WORD),
        ("bmBitsPixel", wintypes.WORD),
        ("bmBits", ctypes.c_void_p),
    ]


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]


class ICONINFO(ctypes.Structure):
    _fields_ = [
        ("fIcon", wintypes.BOOL),
        ("xHotspot", wintypes.DWORD),
        ("yHotspot", wintypes.DWORD),
        ("hbmMask", wintypes.HBITMAP),
        ("hbmColor", wintypes.HBITMAP),
    ]


if app.platform == "windows":
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    gdi32 = ctypes.WinDLL("gdi32")
    shell32 = ctypes.WinDLL("shell32")

    user32.SendMessageTimeoutW.argtypes = [
        wintypes.HWND,
        wintypes.UINT,
        wintypes.WPARAM,
        wintypes.LPARAM,
        wintypes.UINT,
        wintypes.UINT,
        ctypes.POINTER(ctypes.c_size_t),
    ]
    user32.SendMessageTimeoutW.restype = wintypes.LPARAM
    user32.GetClassLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.GetClassLongPtrW.restype = ctypes.c_size_t
    user32.GetIconInfo.argtypes = [wintypes.HICON, ctypes.POINTER(ICONINFO)]
    user32.GetDC.argtypes = [wintypes.HWND]
    user32.GetDC.restype = wintypes.HDC
    user32.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
    gdi32.GetObjectW.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p]
    gdi32.GetDIBits.argtypes = [
        wintypes.HDC,
        wintypes.HBITMAP,
        wintypes.UINT,
        wintypes.UINT,
        ctypes.c_void_p,
        ctypes.POINTER(BITMAPINFOHEADER),
        wintypes.UINT,
    ]
    gdi32.DeleteObject.argtypes = [wintypes.HANDLE]

IID_IShellItemImageFactory = "{bcc18b79-ba16-442f-80c4-8a59c30c463b}"


# Shell icons by (parsing name, size); they only change when apps are updated.
_shell_cache: dict[tuple[str, int], "Icon"] = {}


class Icon:
    """Straight (unmultiplied) RGBA pixels, rows top to bottom."""

    def __init__(self, width: int, height: int, rgba: bytes):
        self.width = width
        self.height = height
        self.rgba = rgba


def bitmap_bgra(hbitmap) -> tuple[int, int, bytearray] | None:
    """The bitmap's pixels as 32-bit top-down BGRA."""
    bm = BITMAP()
    if not gdi32.GetObjectW(hbitmap, ctypes.sizeof(bm), ctypes.byref(bm)):
        return None
    width, height = bm.bmWidth, abs(bm.bmHeight)
    header = BITMAPINFOHEADER()
    header.biSize = ctypes.sizeof(header)
    header.biWidth = width
    header.biHeight = -height
    header.biPlanes = 1
    header.biBitCount = 32
    header.biCompression = BI_RGB
    buf = (ctypes.c_ubyte * (width * height * 4))()
    dc = user32.GetDC(None)
    try:
        lines = gdi32.GetDIBits(dc, hbitmap, 0, height, buf, ctypes.byref(header), DIB_RGB_COLORS)
    finally:
        user32.ReleaseDC(None, dc)
    if lines != height:
        return None
    return width, height, bytearray(buf)


def to_rgba(width: int, height: int, bgra: bytearray, premultiplied: bool) -> Icon:
    pixels = bgra
    pixels[0::4], pixels[2::4] = pixels[2::4], pixels[0::4]
    alpha = pixels[3::4]
    if not any(alpha):
        pixels[3::4] = b"\xff" * (width * height)
    elif premultiplied:
        for i in range(0, len(pixels), 4):
            a = pixels[i + 3]
            if 0 < a < 255:
                pixels[i] = min(pixels[i] * 255 // a, 255)
                pixels[i + 1] = min(pixels[i + 1] * 255 // a, 255)
                pixels[i + 2] = min(pixels[i + 2] * 255 // a, 255)
    return Icon(width, height, bytes(pixels))


def hicon_pixels(hicon) -> Icon | None:
    """Pixels of an HICON; the icon itself stays owned by the caller."""
    info = ICONINFO()
    if not user32.GetIconInfo(hicon, ctypes.byref(info)):
        return None
    try:
        if not info.hbmColor:
            return None
        color = bitmap_bgra(info.hbmColor)
        if color is None:
            return None
        width, height, bgra = color
        if not any(bgra[3::4]) and info.hbmMask:
            # Old-style icon without alpha: the AND mask is white where transparent.
            mask = bitmap_bgra(info.hbmMask)
            if mask is not None and mask[0] == width:
                bgra[3::4] = bytes(0 if m else 255 for m in mask[2][0::4][: width * height])
        return to_rgba(width, height, bgra, premultiplied=False)
    finally:
        if info.hbmColor:
            gdi32.DeleteObject(info.hbmColor)
        if info.hbmMask:
            gdi32.DeleteObject(info.hbmMask)


@on_com_thread
def shell_pixels(parsing_name: str, size: int = ICON_SIZE, thumbnail: bool = False) -> Icon | None:
    """The shell's icon for a file path or shell:AppsFolder\\<AppUserModelID>; with
    `thumbnail`, an image file's own picture instead of its file type's icon.

    On the switcher's COM thread: initializing COM on Talon's own threads can crash
    Talon.
    """
    factory = shell_com.create_item(parsing_name, IID_IShellItemImageFactory)
    if factory is None:
        return None
    hbitmap = wintypes.HBITMAP()
    try:
        # IShellItemImageFactory::GetImage
        hr = shell_com.call(
            factory,
            3,
            shell_com.HRESULT,
            wintypes.SIZE(size, size),
            ctypes.c_int((SIIGBF_THUMBNAILONLY if thumbnail else SIIGBF_ICONONLY) | SIIGBF_BIGGERSIZEOK),
            shell_com.ref(hbitmap),
        )
    finally:
        shell_com.release(factory)
    if hr != 0 or not hbitmap:
        return None
    try:
        pixels = bitmap_bgra(hbitmap)
    finally:
        gdi32.DeleteObject(hbitmap)
    if pixels is None:
        return None
    return to_rgba(*pixels, premultiplied=True)


def window_hicon(hwnd: int):
    """The window's own icon handle (not ours to destroy), or None."""
    for kind in (ICON_BIG, ICON_SMALL2, ICON_SMALL):
        result = ctypes.c_size_t()
        if user32.SendMessageTimeoutW(
            hwnd, WM_GETICON, kind, 0, SMTO_ABORTIFHUNG, 100, ctypes.byref(result)
        ) and result.value:
            return result.value
    for index in (GCLP_HICON, GCLP_HICONSM):
        hicon = user32.GetClassLongPtrW(hwnd, index)
        if hicon:
            return hicon
    return None


def window_icon(
    hwnd: int,
    exe: str | None,
    model_id: str | None,
    size: int = ICON_SIZE,
    own_first: bool = False,
    document: str | None = None,
    own_min: int = 48,
) -> Icon | None:
    """The best icon we can find for a window: the file its host process opened (an MMC
    console's .msc, a Control Panel applet's .cpl), packaged app, then executable, then
    window.

    With `own_first`, the window's own icon comes first if it's at least `own_min`
    pixels: a browser sets a PWA window's icon to the site's, while the shell may only
    have a placeholder letter tile for the PWA's AppUserModelID. Control Panel applets'
    windows have their applet's icon, often only 32 pixels.
    """
    if own_first:
        hicon = window_hicon(hwnd)
        icon = hicon_pixels(hicon) if hicon else None
        if icon is not None and icon.width >= own_min:
            return icon
    names = [document] if document else []
    if model_id:
        names.append(f"shell:AppsFolder\\{model_id}")
    if exe and not exe.lower().endswith("applicationframehost.exe"):
        names.append(exe)
    for name in names:
        key = (name.lower(), size)
        if key in _shell_cache:
            return _shell_cache[key]
        try:
            icon = shell_pixels(name, size)
        except OSError as e:
            print(f"thumbnail_switcher: icon for {name!r}: {e!r}")
            icon = None
        if icon is not None:
            _shell_cache[key] = icon
            return icon
    hicon = window_hicon(hwnd)
    return hicon_pixels(hicon) if hicon else None


@on_com_thread
def shell_display_name(parsing_name: str) -> str | None:
    """The shell's name for a path or shell:AppsFolder\\<AppUserModelID>: the name the
    taskbar and Start show, e.g. "Slack" for a PWA hosted by Microsoft Edge."""
    item = shell_com.create_item(parsing_name)
    if item is None:
        return None
    try:
        return shell_com.item_name(item)
    finally:
        shell_com.release(item)


# Start menu names come from the shared index of installed apps (shell_apps.py).


@on_com_thread
def apps_folder_names() -> dict[str, str]:
    """File path (lowercase) -> Start menu name, for unpackaged apps and MMC consoles."""
    return shell_apps.names_by_path()


@on_com_thread
def apps_folder_name(path: str) -> str | None:
    """The Start menu name for an executable or console (see shell_apps.name_for_path)."""
    return shell_apps.name_for_path(path)


@on_com_thread
def shortcut_names_by_id() -> dict[str, str]:
    """AppUserModelID (lowercase) -> Start menu shortcut name, for shortcuts that set one."""
    return shell_apps.shortcut_names_by_id()
