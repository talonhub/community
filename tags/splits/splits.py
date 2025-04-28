from talon import Module

mod = Module()
mod.tag("splits", desc="Tag for enabling generic window split commands")


@mod.action_class
class Actions:
    def split_window_right():
        """Move active tab to right split"""

    def split_window_left():
        """Move active tab to left split"""

    def split_window_down():
        """Move active tab to lower split"""

    def split_window_up():
        """Move active tab to upper split"""

    def split_window_vertical_line():
        """Splits the window using a vertical split line"""

    def split_window_horizontal_line():
        """Splits the window using a horizontal split line"""

    def split_flip():
        """Flips the orietation of the active split"""

    def split_maximize():
        """Maximizes the active split"""

    def split_reset():
        """Resets the split sizes"""

    def split_window():
        """Splits the window"""

    def split_clear():
        """Clears the current split"""

    def split_clear_all():
        """Clears all splits"""

    def split_next():
        """Goes to next split"""

    def split_last():
        """Goes to last split"""

    def split_number(index: int):
        """Navigates to a the specified split"""
