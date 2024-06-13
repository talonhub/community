from talon import Module, actions, app, settings

mod = Module()

mod.setting(
    "tab_name_format",
    type=str,
    default="ALL_CAPS,DASH_SEPARATED",
    desc="Default format of renamed tab names in an app",
)


# See app.tab_... functions for actions native to talon
@mod.action_class
class TabActions:
    # Creation
    def tab_open_with_name(name: str = ""):
        """Opens a tab renamed to the specified"""

    def tab_clone():
        """Duplicates the current tab"""

    # Destruction
    def tab_close_all():
        """Closes all tabs"""

    def tab_close_others():
        """Closes all tabs but the focused one"""

    def tab_close_wrapper():
        """Closes the current tab

        Exists so that apps can implement their own delay before running
        tab_close() to handle repetitions better
        """
        actions.app.tab_close()

    # Navigation
    def tab_focus_index(index: int):
        """Focuses on the tab at the specified index"""

    def tab_focus_negative_index(index: int):
        """Focuses on the tab at the specified index, indexed from the end"""

    def tab_focus_next():
        """Focuses on the next tab"""
        actions.app.tab_next()

    def tab_focus_previous():
        """Focuses on the previous tab"""
        actions.app.tab_previous()

    def tab_focus_first():
        """Focuses on the first tab"""

    def tab_focus_final():
        """Focuses on the final tab"""

    def tab_focus_most_recent():
        """Focuses on the most recently viewed tab"""

    def tab_focus_named(name: str = ""):
        """Focuses on a tab that matches a specified name"""

    def tab_search(name: str = ""):
        """Searches through the tabs for the specified name"""

    # Arrangement
    def tab_pin():
        """Pins the current tab"""

    def tab_unpin():
        """Unpins the current tab"""

    def tab_move_left():
        """Moves the current tab to the left"""

    def tab_move_right():
        """Moves the current tab to the right"""

    def tab_move_to_split_left():
        """Moves the current tab to the split on the left

        This is only applicable to editors that have split groups that contain tabs, such
        as vscode, jetbrains, etc."""

    def tab_move_to_split_right():
        """Moves the current tab to the split on the right

        This is only applicable to editors that have split groups that contain tabs, such
        as vscode, jetbrains, etc."""

    def tab_move_to_split_up():
        """Moves the current tab to the split above

        This is only applicable to editors that have split groups that contain tabs, such
        as vscode, jetbrains, etc."""

    def tab_move_to_split_down():
        """Moves the current tab to the split below

        This is only applicable to editors that have split groups that contain tabs, such
        as vscode, jetbrains, etc."""

    # Renaming
    def tab_rename(name: str = ""):
        """Renames the current tab"""

    def tab_rename_formatted(name: str = ""):
        """Applies formatting to tab name prior to passing to tab_rename()"""
        if len(name):
            name = actions.user.formatted_text(name, actions.user.tab_name_format())
        actions.user.tab_rename(name)

    def tab_name_reset():
        """Resets the name of the current tab"""

    def tab_name_format():
        """Formatters for tab names in given app"""
        return settings.get("user.tab_name_format")


@mod.action_class
class DeprecatedTabActions:
    def tab_jump(number: int):
        """Jumps to the specified tab"""
        actions.deprecate_action("2024-05-27", "user.tab_jump")

    def tab_final():
        """Jumps to the final tab"""
        actions.deprecate_action("2024-05-27", "user.tab_final")

    def tab_duplicate():
        """Duplicates the current tab"""
        actions.deprecate_action("2024-05-27", "user.tab_duplicate")
