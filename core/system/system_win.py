import ctypes
import os
from typing import TYPE_CHECKING

from talon import Context, actions, app

if app.platform == "windows" or TYPE_CHECKING:
    from ctypes import wintypes

    import win32com.client
    import win32con

    user32 = ctypes.windll.user32

ctx = Context()
ctx.matches = r"""
os: windows
"""


@ctx.action_class("user")
class UserActions:
    def system_switch_screen_power(on: bool):
        """Turns all screens off, or, if all are off, turns those on that were on when having turned all off."""

        user32.GetKeyState.argtypes = [ctypes.c_int]
        user32.GetKeyState.restype = wintypes.SHORT
        user32.GetDesktopWindow.argtypes = []
        user32.GetDesktopWindow.restype = wintypes.HWND
        user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]  # fmt: skip
        user32.DefWindowProcW.restype = ctypes.c_ssize_t

        if on:
            # When testing this on Windows 11 24H2, simulated mouse movement didn't turn the screens on. However, simulated key presses did. The algorithm settled on, that should have as few side effects as possible, followed these thoughts:
            #
            # - `super` activates the Windows start menu.
            # - Some apps react on `ctrl` on its own.
            # - `alt` activates the menu bar.
            # - Besides `capslock`, `shift` *may* be the key that deactivates caps lock, no matter the combination with other modifiers.
            # - The user may have defined a trigger consisting of multiple modifier keys for something like AI-based speech-to-text. They will most likely be near each other on the keyboard. But then again, the same modifier on the left and on the right may be treated as identical.

            def has_capslock():
                return user32.GetKeyState(win32con.VK_CAPITAL) & 1

            had_capslock = has_capslock()

            # When this doesn't turn the screens on, try holding the key for the shortest duration that reliably does the job.
            actions.key("shift:down")
            # actions.sleep("100ms")
            actions.key("shift:up")

            if has_capslock() != had_capslock:
                # Restore state.
                actions.key("capslock")
        else:
            # Turning the screens on via WinAPI call worked for the author on Windows 10, but didn't anymore on Windows 11 24H2. There may be a slim chance that Microsoft fixes this, at least for a UIAccess app like Talon.
            power_code = -1 if on else 2

            # Docs: <https://learn.microsoft.com/en-us/windows/win32/menurc/wm-syscommand#sc_monitorpower>
            # The remarks section says: "An application can carry out any system command at any time by passing a WM_SYSCOMMAND message to DefWindowProc."
            # The window handle doesn't seem to matter, but we choose the one at the very top of the hierarchy that'll always be available.
            user32.DefWindowProcW(
                user32.GetDesktopWindow(),
                win32con.WM_SYSCOMMAND,
                win32con.SC_MONITORPOWER,
                power_code,
            )

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
        shell = win32com.client.Dispatch("Shell.Application")
        shell.ShutdownWindows()
