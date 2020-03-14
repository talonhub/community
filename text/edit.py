from talon import Module

mod = Module()


@mod.action_class
class Actions:
    def drag_up():
         """Trigger auto complete in the ide (intellijsense)"""

    def drag_down():
         """Trigger better auto complete in the ide"""

    def clone_line():
        """Duplicate the current line"""

    def multi_cursor():
        """Activate multi cursor mode"""

    def multi_cursor_stop():
        """Deactivate multi cursor mode"""

    def up_cursor():
        """Add a cursor above current cursors"""

    def down_cursor():
        """Add a cursor below current curors"""