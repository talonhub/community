import ctypes
import os
from talon import Context, app
from typing import TYPE_CHECKING

if app.platform == "windows" or TYPE_CHECKING:
    from ctypes import wintypes
    user32 = ctypes.windll.user32

ctx = Context()
ctx.matches = r"""
os: windows
"""


@ctx.action_class("user")
class UserActions:
    def system_switch_screen_power(on: bool):
        """Turns all screens off, or, if all are off, turns those on that were on when having turned all off.

        Turning the screens on didn't work for the author on Windows 11 24H2, even though it worked for him on Windows 10 before when the same call to `DefWindowProcW()` was made in a different programming language. Turning the screens on using code like `actions.mouse_move(actions.mouse_x() + 1, actions.mouse_y() + 1)` also didn't work.
        """

        user32.GetDesktopWindow.argtypes = []
        user32.GetDesktopWindow.restype = wintypes.HWND
        user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]  # fmt: skip
        user32.DefWindowProcW.restype = ctypes.c_ssize_t

        WM_SYSCOMMAND = 0x112
        SC_MONITORPOWER = 0xF170

        power_code = -1 if on else 2
        user32.DefWindowProcW(
            user32.GetDesktopWindow(), WM_SYSCOMMAND, SC_MONITORPOWER, power_code
        )

        # Docs: <https://learn.microsoft.com/en-us/windows/win32/menurc/wm-syscommand#sc_monitorpower>
        # The remarks section says: "An application can carry out any system command at any time by passing a WM_SYSCOMMAND message to DefWindowProc."
        # The window handle doesn't seem to matter, but we choose the one at the very top of the hierarchy that'll always be available.

    def system_show_settings():
        os.startfile("ms-settings:")

    def system_lock():
        user32.LockWorkStation.argtypes = []
        user32.LockWorkStation.restype = wintypes.BOOL

        # More reliable alternative to simulating Win+L.
        success_initiating = user32.LockWorkStation()
        if not success_initiating:
            raise ctypes.WinError()

    def system_show_exit_menu():
        user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
        user32.FindWindowW.restype = wintypes.HWND
        user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]  # fmt: skip
        user32.SendMessageW.restype = ctypes.c_ssize_t

        WM_COMMAND = 0x0111

        taskbar_hwnd = user32.FindWindowW("Shell_TrayWnd", "")
        if not taskbar_hwnd:
            raise OSError("Couldn't find the taskbar window.")

        # Source for command code: <https://www.codeproject.com/articles/Manipulating-The-Windows-Taskbar>
        user32.SendMessageW(taskbar_hwnd, WM_COMMAND, 0x01FA, 0)
