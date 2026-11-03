"""Window icons as RGBA pixels, for tiles whose DWM thumbnail would be blank (minimized).

Large icons come from the shell (IShellItemImageFactory) for the app's AppUserModelID
or executable; the window's own HICON (WM_GETICON, then the class icon) is the fallback.
"""

import ctypes
import os
import re
from ctypes import wintypes

from talon import app

from ..windows import app_icons, shell_apps, shell_com
from ..windows.com_thread import on_com_thread
from ..windows.shell_icons import ICON_SIZE, Icon, hicon_pixels, shell_pixels  # noqa: F401 (callers use window_icons.*)

WM_GETICON = 0x007F
ICON_SMALL = 0
ICON_BIG = 1
ICON_SMALL2 = 2
SMTO_ABORTIFHUNG = 0x0002
GCLP_HICON = -14
GCLP_HICONSM = -34

if app.platform == "windows":
    user32 = ctypes.WinDLL("user32", use_last_error=True)
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
        # Cached (in memory and on disk) by app_icons; fetched here if it isn't yet.
        icon = app_icons.fetch(name, size)
        if icon is not None:
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
