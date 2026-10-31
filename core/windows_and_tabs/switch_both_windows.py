from talon import Module, actions

mod = Module()


@mod.action_class
class WindowActions:
    def switch_both_windows_next_screen():
        """Move this window and the previously focused window to the next screen."""
        actions.user.move_window_next_screen()
        actions.sleep("60ms")
        actions.user.switcher_focus_last()
        actions.sleep("60ms")
        actions.user.move_window_next_screen()