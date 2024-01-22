settings():
    # Adjust the scale of the imgui
    imgui.scale = 1.3

    # Automatically show the picker GUI when the file manager has focus
    user.file_manager_auto_show_pickers = false

    # Set the max number of command lines to display per page of help
    user.help_max_command_lines_per_page = 50

    # Set the max number of contexts to display per page of help
    user.help_max_contexts_per_page = 20

    # Set the default scroll amount used when scrolling continuously
    user.mouse_continuous_scroll_amount = 80

    # Stop continuous scroll/gaze scroll with a pop
    user.mouse_enable_pop_stops_scroll = true

    # Choose how pop click should work in 'control mouse' mode
    # 0 = off
    # 1 = on with eyetracker but not zoom mouse mode
    # 2 = on but not with zoom mouse mode
    user.mouse_enable_pop_click = 1

    # Use a hissing noise to scroll continuously
    user.mouse_enable_hiss_scroll = false

    # # Hide the continuous scroll/gaze scroll GUI
    user.mouse_hide_mouse_gui = false

    # Hide the cursor when enabling zoom mouse
    user.mouse_wake_hides_cursor = false

    # Set the amount to scroll up/down (equivalent to mouse wheel on Windows by default)
    user.mouse_wheel_down_amount = 120

    # Set the amount to scroll left/right
    user.mouse_wheel_horizontal_amount = 40

    # Start mouse grid numbering on the bottom left (vs. top left)
    user.grids_put_one_bottom_left = true

    # Set the number of command history lines to display by default
    user.command_history_display = 10

    # Set the total number of command history lines to keep; say "command history more"
    # to display all of them and "command history less" to display the default
    user.command_history_size = 50

    # Uncommment to add a directory (relative to the Talon user dir) with additional
    # .snippet files. Changing this setting requires a restart of Talon.
    # user.snippets_dir = "snippets"

    # Uncomment to insert text longer than 10 characters (customizable) by pasting from
    # the clipboard. This is often faster than typing.
    # user.paste_to_insert_threshold = 10

    # Uncomment to enable context-sensitive dictation. This determines how to format
    # (capitalize, space) dictation-mode speech by selecting & copying surrounding text
    # before inserting. This can be slow and may not work in some applications. You may
    # wish to enable this on a per-application basis.
    # user.context_sensitive_dictation = true

    # Choose how to resize windows moved across physical screens (eg. via `snap next`).
    # Default is 'proportional', which preserves window size : screen size ratio.
    # 'size aware' keeps absolute window size the same, except full-height or
    # -width windows are resized to stay full-height/width.
    # user.window_snap_screen = "size aware"

# Uncomment to enable the curse yes/curse no commands (show/hide mouse cursor).
# See issue #688 for more detail: https://github.com/talonhub/community/issues/688
# tag(): user.mouse_cursor_commands_enable
