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

    # Enable pop click with 'control mouse' mode.
    # 0 = off
    # 1 = on with eyetracker but not zoom mouse mode
    # 2 = on but not with zoom mouse mode
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

    # Uncomment the below to insert text longer than 10 characters (customizable) by
    # pasting from the clipboard. This is often faster than typing.
    #user.paste_to_insert_threshold = 10

    # Uncomment the below to enable context-sensitive dictation. This determines
    # how to format (capitalize, space) dictation-mode speech by selecting &
    # copying surrounding text before inserting. This can be slow and may not
    # work in some applications. You may wish to enable this on a
    # per-application basis.
    # user.context_sensitive_dictation = 1

    # How to resize windows moved across physical screens (eg. via `snap next`).
    # Default is 'proportional', which preserves window size : screen size ratio.
    # 'size aware' keeps absolute window size the same, except full-height or
    # -width windows are resized to stay full-height/width.
    #user.window_snap_screen = "size aware"

# Uncomment this to enable the curse yes/curse no commands (show hide mouse cursor). See issue #688.
# tag(): user.mouse_cursor_commands_enable
