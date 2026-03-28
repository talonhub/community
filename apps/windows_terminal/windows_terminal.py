import os

from talon import Context, Module, actions, ui

ctx = Context()
mod = Module()
ctx.matches = r"""
app: windows_terminal
"""


@ctx.action_class("app")
class AppActions:
    def tab_close():
        actions.key("ctrl-shift-w")

    def tab_open():
        actions.key("ctrl-shift-t")


@ctx.action_class("edit")
class EditActions:
    def paste():
        actions.key("ctrl-shift-v")

    def copy():
        actions.key("ctrl-shift-c")

    def find(text: str = None):
        actions.key("ctrl-shift-f")
        if text:
            actions.insert(text)


@ctx.action_class("user")
class UserActions:

    def tab_jump(number: int):
        actions.key(f"ctrl-alt-{number}")

    # user.splits implementation:

    def split_window_right():
        """Move active tab to right split"""
        actions.app.notify(
            '"Split right" is not possible in windows terminal without special configuration. Use "split vertically" instead.'
        )

    def split_window_left():
        """Move active tab to left split"""
        actions.app.notify(
            '"Split left" is not possible in windows terminal without special configuration. Use "split vertically" instead.'
        )

    def split_window_down():
        """Move active tab to lower split"""
        actions.app.notify(
            '"Split down" is not possible in windows terminal without special configuration. Use "split horizontally" instead.'
        )

    def split_window_up():
        """Move active tab to upper split"""
        actions.app.notify(
            '"Split up" is not possible in windows terminal without special configuration. Use "split horizontally" instead.'
        )

    def split_window_vertically():
        """Splits window vertically"""
        actions.key("shift-alt-plus")

    def split_window_horizontally():
        """Splits window horizontally"""
        actions.key("shift-alt-minus")

    def split_flip():
        """Flips the orietation of the active split"""
        actions.app.notify(
            '"Split flip" is not possible in windows terminal in default configuration.'
        )

    def split_window():
        """Splits the window"""
        # in this implementation an alias for split vertically
        actions.key("shift-alt-plus")

    def split_clear():
        """Clears the current split"""
        # also closes tab, because shortcut is the same
        # and closing a split does mean something differnent that in a code editor like vs code
        actions.key("ctrl-shift-w")

    def split_next():
        """Goes to next split"""
        actions.app.notify(
            '"Split next" is not possible in windows terminal without special configuration. Use "focus left/right/up/down" instead.'
        )

    def split_last():
        """Goes to last split"""
        actions.app.notify(
            '"Split last" is not possible in windows terminal without special configuration. Use "focus left/right/up/down" instead.'
        )

    def split_number(index: int):
        """Navigates to a the specified split"""
        actions.app.notify(
            '"Split_number" is not possible in windows terminal in default configuration.'
        )

    def tab_final():
        actions.key("ctrl-alt-9")
