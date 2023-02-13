from talon import Module, actions, app

mod = Module()

cmd_ctrl = "cmd" if app.platform == "mac" else "ctrl"


@mod.action_class
class tab_actions:
    def tab_jump(number: int):
        """Jumps to the specified tab"""
        if number < 9:
            if app.platform == "linux":
                actions.key(f"alt-{number}")
            else:
                actions.key(f"{cmd_ctrl}-{number}")

    def tab_final():
        """Jumps to the final tab"""
        if app.platform == "linux":
            pass
        else:
            actions.key(f"{cmd_ctrl}-9")

    def tab_close_wrapper():
        """Closes the current tab.
        Exists so that apps can implement their own delay before running tab_close() to handle repetitions better.
        """
        actions.app.tab_close()

    def tab_duplicate():
        """Duplicates the current tab."""
