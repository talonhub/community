"""Icons as RGBA pixels: from the shell (IShellItemImageFactory, for a file path or
shell:AppsFolder\\<AppUserModelID>) and from icon handles.

Shared by the app switcher's tools: app_icons.py caches what shell_pixels finds; the
thumbnail switcher's window_icons.py adds windows' own icons.
"""

import ctypes
from ctypes import wintypes

from talon import app

from . import shell_com
from .com_thread import on_com_thread

ICON_SIZE = 128

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
