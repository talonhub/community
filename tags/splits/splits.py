from talon import Module, actions

mod = Module()
mod.tag("splits", desc="Tag for enabling generic window split commands")


@mod.action_class
class SplitActions:
    # Creation

    ## Empty splits
    def split_create():
        """Creates a new empty split. The default orientation is application dependent"""

    def split_create_right():
        """Create a new empty split to the right"""

    def split_create_left():
        """Create a new empty split to the left"""

    def split_create_down():
        """Create a new empty split to the bottom"""

    def split_create_up():
        """Create a new empty split to the top"""

    def split_create_vertically():
        """Create a new empty vertical split. The left or right orientation is application dependent"""

    def split_create_horizontally():
        """Create a new empty horizontal split. The top or bottom orientation is application dependent"""

    ## Duplicate splits
    def split_clone():
        """Clones the active view into a new split. The default orientation is application dependent"""

    def split_clone_right():
        """Clone the active view into a new split opened to the right"""

    def split_clone_left():
        """Clone the active view into a new split opened to the left"""

    def split_clone_down():
        """Clone the active view into a new split opened to the bottom"""

    def split_clone_up():
        """Clone the active view into a new split opened to the top"""

    def split_clone_vertically():
        """Clone the active view vertically. The left or right orientation is application dependent"""

    def split_clone_horizontally():
        """Clone the active view horizontally. The top or bottom orientation is application dependent"""

    def split_reopen_last():
        """Reopen the most recently closed split at the same orientation"""

    # Destruction
    def split_close():
        """Closes the current split"""

    def split_close_all():
        """Closes all splits"""

    # Navigation
    def split_focus_right():
        """Focus on the split to the right of the current view"""

    def split_focus_left():
        """Focus on the split to the left of the current view"""

    def split_focus_down():
        """Focus on the split below the current view"""

    def split_focus_up():
        """Focus on the split above the current view"""

    def split_focus_next():
        """Focuses on the next available split"""

    def split_focus_previous():
        """Focuses on the previous available split"""

    def split_focus_first():
        """Focuses on the first split"""

    def split_focus_final():
        """Focuses on the final split"""

    def split_focus_most_recent():
        """Focuses on the most recently used split"""

    def split_focus_index(index: int):
        """Focuses on the split at the specified index"""

    def split_focus_negative_index(index: int):
        """Focuses on the split at the specified index, negatively indexed from the end"""

    # Arrangement
    def split_move_right():
        """Move the active split to the right. The creation of a new split is application dependent."""

    def split_move_left():
        """Move the active split to the left. The creation of a new split is application dependent."""

    def split_move_down():
        """Move the active split down. The creation of a new split is application dependent."""

    def split_move_up():
        """Move the active split up. The creation of a new split is application dependent."""

    def split_toggle_zen():
        """Centers the active split (eg: zen mode)"""

    def split_rotate_right():
        """Rotates the splits to the right"""

    def split_rotate_left():
        """Rotates the splits to the left"""

    # Resizing
    def split_toggle_orientation():
        """Flips the orientation of the active split"""

    def split_toggle_maximize():
        """Maximizes the active split"""

    def split_layout_reset():
        """Resets all the split sizes"""

    def split_expand():
        """Expands the both the width and height of the split"""
        actions.user.split_expand_width()
        actions.user.split_expand_height()

    def split_expand_width():
        """Expands the split width"""

    def split_expand_height():
        """Expands the split height"""

    def split_shrink():
        """Shrinks the both the width and height of the split"""
        actions.user.split_shrink_width()
        actions.user.split_shrink_height()

    def split_shrink_width():
        """Shrinks the split width"""

    def split_shrink_height():
        """Shrinks the split height"""

    def split_set_width(width: int):
        """Sets the split width"""

    def split_set_height(height: int):
        """Sets the split height"""

    def split_move_next_tab():
        """Move the current window to the next tab

        This is only applicable to editors that have tabs that contain splits, such
        as neovim, etc"""

    def split_move_previous_tab():
        """Move the current window to the previous tab

        This is only applicable to editors that have tabs that contain splits, such
        as neovim, etc"""

    def split_move_new_tab():
        """Move the current window to a new tab

        This is only applicable to editors that have tabs that contain splits, such
        as neovim, etc"""


@mod.action_class
class DeprecatedSplitActions:
    def split_next():
        """Goes to next split"""
        actions.deprecate_action("2024-05-27", "user.split_next")

    def split_last():
        """Goes to last split"""
        actions.deprecate_action("2024-05-27", "user.split_last")

    def split_number(index: int):
        """Navigates to the specified split"""
        actions.deprecate_action("2024-05-27", "user.split_number")

    def split_window_right():
        """Create a split, of the active window, to the right"""
        actions.deprecate_action("2024-05-27", "user.split_window_right")

    def split_window_left():
        """Create a split, of the active window, to the left"""
        actions.deprecate_action("2024-05-27", "user.split_window_left")

    def split_window_down():
        """Create a split, of the active window, below"""
        actions.deprecate_action("2024-05-27", "user.split_window_down")

    def split_window_up():
        """Create a split, of the active window, above"""
        actions.deprecate_action("2024-05-27", "user.split_window_up")

    def split_window_vertically():
        """Splits window vertically"""
        actions.deprecate_action("2024-05-27", "user.split_window_vertically")

    def split_window_horizontally():
        """Splits window horizontally"""
        actions.deprecate_action("2024-05-27", "user.split_window_horizontally")

    def split_window():
        """Splits the window"""
        actions.deprecate_action("2024-05-27", "user.split_window")

    def split_clear():
        """Closes the current split"""
        actions.deprecate_action("2024-05-27", "user.split_clear")

    def split_clear_all():
        """Closes all splits"""
        actions.deprecate_action("2024-05-27", "user.split_clear_all")

    def split_flip():
        """Flips the orientation of the active split"""
        actions.deprecate_action("2024-05-27", "user.split_flip")

    def split_maximize():
        """Maximizes the active split"""
        actions.deprecate_action("2024-05-27", "user.split_maximize")

    def split_reset():
        """Resets all the split sizes"""
        actions.deprecate_action("2024-05-27", "user.split_reset")
