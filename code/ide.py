from talon import Module

mod = Module()


@mod.action_class
class Actions:
    def ide_refactor():
        """Trigger refactoring menu of the ide"""

    def ide_complete():
         """Trigger auto complete in the ide (intellijsense)"""

    def ide_perfect():
         """Trigger better auto complete in the ide"""

    def ide_smart():
         """Trigger type completion in the ide"""

    def ide_finish():
        """Select auto complete statement"""

    def ide_done():
        """Select auto complete statement"""

    def ide_toggle_tools():
         """Hide all windows"""

    def ide_extract_variable():
        """Trigger extract variable functionality of IDE"""

    def ide_extract_field():
        """Trigger extract field functionality of IDE"""

    def ide_extract_constant():
        """Trigger extract constant functionality of IDE"""

    def ide_extract_parameter():
        """Trigger extract parameter functionality of IDE"""

    def ide_extract_interface():
        """Trigger extract interface functionality of IDE"""

    def ide_extract_method():
        """Trigger extract method functionality of IDE"""

    def ide_refactor_in_line():
        """Trigger inline refactoring method of IDE"""

    def ide_refactor_move():
        """Trigger refactor move functionality of IDE"""

    def ide_refactor_rename():
        """Trigger refactor rename functionality of IDE"""

    def ide_rename_file():
        """Trigger rename file of IDE"""

    def ide_fix_format():
        """Trigger format code function"""

    def ide_fix_imports():
        """Trigger fix imports function"""

    def ide_follow():
        """Go to definition of selected item"""

    def ide_go_implementation():
        """Go to implementation of selected item"""

    def ide_go_usage():
        """Go to usage of selected item"""

    def ide_go_type():
        """Go to type of selected item"""

    def ide_go_test():
        """Go to test of selected item"""

    def ide_go_back():
        """Go to previous cursor position"""

    def ide_go_forward():
        """Go to next"""

    def ide_find_everywhere():
        """Searches the entire project"""

    def ide_find_class():
        """Open search for class functionality of ide"""

    def ide_find_in_path():
        """Open search filtered to selected path"""

    def ide_find_file():
        """Open search for file functionality of ide"""

    def ide_recent():
        """Open recent files list"""

    def ide_drag_up():
         """Trigger auto complete in the ide (intellijsense)"""

    def ide_drag_down():
         """Trigger better auto complete in the ide"""

    def ide_clone_line():
        """Duplicate the current line"""

    def ide_multi_cursor():
        """Activate multi cursor mode"""

    def ide_multi_cursor_stop():
        """Deactivate multi cursor mode"""

    def ide_up_cursor():
        """Add a cursor above current cursors"""

    def ide_down_cursor():
        """Add a cursor below current cursors"""

    def ide_select_less():
        """Unselect current word"""

    def ide_select_more():
        """Select next word"""

    def ide_multi_select_fewer():
        """Unselect previously selected word"""

    def ide_multi_select_more():
        """Select next occurrence of word"""

    def ide_multi_select_all():
        """Select all occurrences of word"""

