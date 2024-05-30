from talon import Module, actions, settings

mod = Module()

mod = Module()
mod.setting(
    "tab_name_format",
    type=str,
    default="ALL_CAPS,DASH_SEPARATED",
    desc="Default format of renamed tab names in an app",
)


@mod.action_class
class tab_actions:
    def tab_jump(number: int):
        """Jumps to the specified tab"""

    def tab_final():
        """Jumps to the final tab"""

    def tab_close_wrapper():
        """Closes the current tab.
        Exists so that apps can implement their own delay before running tab_close() to handle repetitions better.
        """
        actions.app.tab_close()

    def tab_duplicate():
        """Duplicates the current tab."""

    def tab_search():
        """Searches through the tabs."""

    def tab_pin():
        """Pins the current tab."""

    def tab_unpin():
        """Unpins the current tab."""

    def tab_rename_wrapper(name: str):
        """Applies formatting to tab name prior to passing to overridden tab_rename()"""
        if len(name):
            name = actions.user.formatted_text(name, actions.user.tab_name_format())
        actions.app.tab_rename(name)

    def tab_rename(name: str):
        """Renames the current tab."""

    def tab_name_format():
        """Formatters for tab names in given app"""
        return settings.get("user.tab_name_format")

    def tab_focus_most_recent():
        """Jumps to the most recently viewed tab."""

    def tab_move_left():
        """Moves the current tab to the left."""

    def tab_move_right():
        """Moves the current tab to the right."""
