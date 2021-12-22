-
settings():
    # Adjust the scale of the imgui to my liking
    imgui.scale = 1.3

    # Enable if you'd like the picker gui to automatically appear when explorer has focus
    user.file_manager_auto_show_pickers = 0

    # Set the max number of command lines per page in help
    user.help_max_command_lines_per_page = 50

    # Set the max number of contexts display per page in help
    user.help_max_contexts_per_page = 20

    # The default amount used when scrolling continuously
    user.mouse_continuous_scroll_amount = 80

    # Stop continuous scroll/gaze scroll with a pop
    user.mouse_enable_pop_stops_scroll = 1

    # Enable pop click with 'control mouse' mode
    user.mouse_enable_pop_click = 1

    # When enabled, the 'Scroll Mouse' GUI will not be shown.
    user.mouse_hide_mouse_gui = 0

    # Hide cursor when mouse_wake is called to enable zoom mouse
    user.mouse_wake_hides_cursor = 0

    # The amount to scroll up/down (equivalent to mouse wheel on Windows by default)
    user.mouse_wheel_down_amount = 120

    # The amount to scroll left/right
    user.mouse_wheel_horizontal_amount = 40

    # Mouse grid and friends put the number one on the bottom left (vs on the top left)
    user.grids_put_one_bottom_left = 1

    # The number of lines of command history to display by default
    user.command_history_display = 10

    # The number of lines of command history to keep in total;
    # "command history more" to display all of them, "command history less" to restore
    user.command_history_size = 50

    # Uncomment the below to enable context-sensitive dictation. This determines
    # how to format (capitalize, space) dictation-mode speech by selecting &
    # copying surrounding text before inserting. This can be slow and may not
    # work in some applications. You may wish to enable this on a
    # per-application basis.
    # user.context_sensitive_dictation = 1

    # The update frequency used when moving a window continuously
    user.win_move_frequency = "60ms"

    # The target speed, in cm/sec, for continuous move operations
    user.win_continuous_move_rate = 4.1

    # When enabled, the 'Move/Resize Window' GUI will not be shown for continuous move operations
    user.win_hide_move_gui = 0

    # The update frequency used when resizing a window continuously
    # note: setting this value too low may result in
    user.win_resize_frequency = "60ms"

    # The target speed, in cm/sec, for continuous resize operations
    user.win_continuous_resize_rate = 4.0

    # When enabled, the 'Move/Resize Window' GUI will not be shown for continuous resize operations
    user.win_hide_resize_gui = 0

    # How long to wait (in seconds) for talon to signal completion of window move/resize requests
    user.win_set_queue_timeout = 0.2

    # How many times to retry a timed out talon window move/resize request
    user.win_set_retries = 1

    # Whether to generate warnings for anomalous events.
    user.win_verbose_warnings = 0

# Uncomment this to enable the curse yes/curse no commands (show hide mouse cursor). See issue #688.
# tag(): user.mouse_cursor_commands_enable
