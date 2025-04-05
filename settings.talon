-
settings():
    tracking.zoom_live = false
    tracking.zoom_width = 800
    tracking.zoom_height = 600
    tracking.zoom_scale = 3

    speech.record_all = 1
    speech.timeout = .400
    user.listening_timeout_minutes = 3
    # Adjust the scale of the imgui to my liking
    imgui.scale = 2.5
    user.snippets_dir = "snippets"
    # Enable if you'd like the picker gui to automatically appear when explorer has focus

    # Set the max number of command lines per page in help
    user.help_max_command_lines_per_page = 50

    # Set the max number of contexts display per page in help
    user.help_max_contexts_per_page = 20

    # The default amount used when scrolling continuously
    user.mouse_continuous_scroll_amount = 8

    # Stop continuous scroll/gaze scroll with a pop
    user.mouse_enable_pop_stops_scroll = true

    # Enable pop click with 'control mouse' mode.
    # 0 = off
    # 1 = on with eyetracker but not zoom mouse mode
    # 2 = on but not with zoom mouse mode
    user.mouse_enable_pop_click = 1

    # Enable if you like to use the hissing noise to do mouse scroll
    # user.mouse_enable_hiss_scroll = false

    # When enabled, the 'Scroll Mouse' GUI will not be shown.
    user.mouse_hide_mouse_gui = false

    # Hide cursor when mouse_wake is called to enable zoom mouse
    user.mouse_wake_hides_cursor = false

    # The amount to scroll up/down (equivalent to mouse wheel on Windows by default)
    user.mouse_wheel_down_amount = 120

    # The amount to scroll left/right
    user.mouse_wheel_horizontal_amount = 40

    # Mouse grid and friends put the number one on the bottom left (vs on the top left)
    user.grids_put_one_bottom_left = true

    # The number of lines of command history to display by default
    user.command_history_display = 10

    # The number of lines of command history to keep in total;
    # "command history more" to display all of them, "command history less" to restore
    user.command_history_size = 50

    # Uncomment the below line to add a directory (relative to the Talon user dir) with additional .snippet files
    # Changing this setting requires a restart of Talon
    # user.snippets_dir = "snippets"

    # Uncomment the below to insert text longer than 10 characters (customizable) by
    # pasting from the clipboard. This is often faster than typing.
    user.paste_to_insert_threshold = -1
    # Uncomment the below to enable context-sensitive dictation. This determines
    # how to format (capitalize, space) dictation-mode speech by selecting &
    # copying surrounding text before inserting. This can be slow and may not
    # work in some applications. You may wish to enable this on a
    # per-application basis.
    user.context_sensitive_dictation = true

    # How to resize windows moved across physical screens (eg. via `snap next`).
    # Default is 'proportional', which preserves window size : screen size ratio.
    # 'size aware' keeps absolute window size the same, except full-height or
    # -width windows are resized to stay full-height/width.
    #user.window_snap_screen = "size aware"

# Uncomment this to enable the curse yes/curse no commands (show hide mouse cursor). See issue #688.
# tag(): user.mouse_cursor_commands_enable
# tag():user.mouse_grid_enabled
tag(): user.talon_populate_lists
# tag(): talon_plugins.eye_zoom_mouse.zoom_mouse_noise
tag(): user.experimental_window_layout
# tag(): user.mouse_grid_enabled