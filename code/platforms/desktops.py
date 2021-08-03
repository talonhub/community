from talon import Module

mod = Module()

@mod.action_class
class Actions:
    def desktop(number: int):
        """change the current desktop"""

    def desktop_show():
        """shows the current desktops"""

    def desktop_next():
        """move to next desktop"""

    def desktop_last():
        """move to previous desktop"""

    def window_move_desktop_left():
        """move the current window to the desktop to the left"""

    def window_move_desktop_right():
        """move the current window to the desktop to the right"""

    def window_move_desktop(desktop_number: int):
        """move the current window to a different desktop"""
