from talon import app, Module

mod = Module()

@mod.action_class
class Actions:
    def desktop(number: int):
        """change the current desktop"""
        app.notify("Not supported on this operating system")

    def desktop_show():
        """shows the current desktops"""
        app.notify("Not supported on this operating system")

    def desktop_next():
        """move to next desktop"""
        app.notify("Not supported on this operating system")

    def desktop_last():
        """move to previous desktop"""
        app.notify("Not supported on this operating system")

    def window_move_desktop_left():
        """move the current window to the desktop to the left"""
        app.notify("Not supported on this operating system")

    def window_move_desktop_right():
        """move the current window to the desktop to the right"""
        app.notify("Not supported on this operating system")

    def window_move_desktop(desktop_number: int):
        """move the current window to a different desktop"""
        app.notify("Not supported on this operating system")
