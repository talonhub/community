from talon import Context, actions, ui, Module, app

mod = Module()
mod.tag("multiple_cursors", desc="Tag for enabling generic multiple cursor commands")


@mod.action_class
class multiple_cursor_actions:
    def multi_cursor_enable():
        """Enables multi-cursor mode"""

    def multi_cursor_disable():
        """Disables multi-cursor mode"""

    def multi_cursor_add_above():
        """Adds cursor to line above"""

    def multi_cursor_add_below():
        """Adds cursor to line below"""

    def multi_cursor_select_fewer_occurrences():
        """Removes selection & cursor at last occurrence"""

    def multi_cursor_select_more_occurrences():
        """Adds cursor at next occurrence of selection"""

    def multi_cursor_skip_occurrence():
        """Skips adding a cursor at next occurrence of selection"""

    def multi_cursor_select_all_occurrences():
        """Adds cursor at every occurrence of selection"""

    def multi_cursor_add_to_line_ends():
        """Adds cursor at end of every selected line"""
