settings():
    # Adjust the scale of the imgui
    imgui.scale = 1.3

    # Uncomment to set the speech timeout. This is the amount of time after you stop
    # speaking until Talon starts processing the spoken audio. Default is 0.3s.
    # speech.timeout = 0.3

    # Uncomment to enable dark mode for talon help menus
    # imgui.dark_mode = true

    # If `true`, automatically show the picker GUI when the file manager has focus
    user.file_manager_auto_show_pickers = false

    # Set the number of command lines to display per help page
    user.help_max_command_lines_per_page = 50

    # Set the number of contexts to display per help page
    user.help_max_contexts_per_page = 20

    # Uncomment to always sort help contexts alphabetically.
    # user.help_sort_contexts_by_specificity = false

    # Set the scroll amount for continuous scroll
    user.mouse_continuous_scroll_amount = 8

    # Set the scroll multiplier for gaze scroll
    user.mouse_gaze_scroll_speed_multiplier = 1.0

    # Set the maximum acceleration factor when scrolling continuously. 1=constant speed/no acceleration.
    user.mouse_continuous_scroll_acceleration = 1

    # If `true`, stop continuous scroll/gaze scroll with a pop
    user.mouse_enable_pop_stops_scroll = true

    # If `true`, stop mouse drag with a pop
    user.mouse_enable_pop_stops_drag = true

    # Choose how pop click should work in 'control mouse' mode
    # 0 = off
    # 1 = on with eyetracker but not zoom mouse mode
    # 2 = on but not with zoom mouse mode
    user.mouse_enable_pop_click = 1

    # If `true`, use a hissing noise to scroll continuously
    user.mouse_enable_hiss_scroll = false

    # How much time a hiss must last for to be considered a hiss rather than
    # part of speech, in ms
    user.hiss_scroll_debounce_time = 100

    # If `true`, hide the continuous scroll/gaze scroll GUI
    user.mouse_hide_mouse_gui = false

    # If `true`, hide the cursor when enabling zoom mouse
    user.mouse_wake_hides_cursor = false

    # Set the amount to scroll up/down
    user.mouse_wheel_down_amount = 120

    # Set the amount to scroll left/right
    user.mouse_wheel_horizontal_amount = 40

    # If `true`, start mouse grid numbering on the bottom left (vs. top left)
    user.grids_put_one_bottom_left = true

    # Set the default number of command history lines to display
    user.command_history_display = 10

    # Set the total number of command history lines to display
    user.command_history_size = 50

    # Set the time window size for to for pop_twice_to_sleep and pop_twice_to_repeat. By default, the pops must be more than 0.1 seconds apart and less then 0.3 seconds, to reduce false positives
    user.double_pop_speed_minimum = 0.1
    user.double_pop_speed_maximum = 0.3

    # Uncomment to add a directory (relative to the Talon user dir) with additional
    # .snippet files. Changing this setting requires a restart of Talon.
    # user.snippets_dir = "snippets"

    # Set the number of spaces to convert each tab to for inserting snippets without editor support. A negative number means that tabs will not be converted to spaces. This setting should be set to a negative number for actual code editors because they can format tabs correctly. This setting is available for contexts like web browsers and chat applications that do not understand code formatting.
    user.snippet_raw_text_spaces_per_tab = 4

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

    # Puts Talon into sleep mode if no commands are spoken for a defined period of time.
    # user.listening_timeout_minutes = 3

    # Time in seconds to wait for the clipboard to change when trying to get selected text
    # user.selected_text_timeout = 0.25

# Uncomment to enable the curse yes/curse no commands (show/hide mouse cursor).
# See issue #688 for more detail: https://github.com/talonhub/community/issues/688
# tag(): user.mouse_cursor_commands_enable

# Uncomment below enable pop_twice_to_wake
# Without this tag noise_trigger_pop is usually associated with pop to click actions
# Enabling this tag disables other pop to click actions in sleep mode, including pop to click
# tag(): user.pop_twice_to_wake

# Uncomment below enable pop_twice_to_repeat
# Enabling this tag will repeat the last command when two pops are heard within the allotted time window
# Without this tag noise_trigger_pop is usually associated with pop to click actions
# Enabling this tag disables other pop to click actions in command mode, including pop to click
# tag(): user.pop_twice_to_repeat

# Uncomment the below to enable support for saying numbers without a prefix.
# By default you need to say "numb one" to write "1". If you uncomment this,
# you can say "one" to write "1".
# tag(): user.unprefixed_numbers

# Uncomment the below to enable the experimental window layout commands
# defined in window_layout.talon
# tag(): user.experimental_window_layout
