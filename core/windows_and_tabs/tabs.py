from talon import Module, actions, app

mod = Module()


@mod.action_class
class tab_actions:
    def tab_close_wrapper():
        """Closes the current tab.
        Exists so that apps can implement their own delay before running tab_close() to handle repetitions better.
        """
        actions.app.tab_close()

    def tab_duplicate():
        """Duplicates the current tab"""

    def tab_final():
        """Jumps to the final tab"""

    def tab_jump(number: int):
        """Jumps to a tab by its one-based index"""

    def tab_move_left():
        """Move the current tab one tab to the left"""

    def tab_move_right():
        """Move the current tab one tab to the right"""

    def tab_switcher_focus(text: str):
        """Focus a tab using tab search"""

    def tab_switcher_focus_last():
        """Focus last tab"""

    def tab_switcher_menu():
        """Shows the app's tab switcher"""
