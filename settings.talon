-
settings():
    #adjust the scale of the imgui to my liking
    imgui.scale = 1.3
    # enable if you'd like the picker gui to automatically appear when explorer has focus
    user.file_manager_auto_show_pickers = 0
    #set the max number of command lines per page in help
    user.help_max_command_lines_per_page = 50
    # set the max number of contexts display per page in help
    user.help_max_contexts_per_page = 20
    # The default amount used when scrolling continuously
    user.mouse_continuous_scroll_amount = 80
    #stop continuous scroll/gaze scroll with a pop
	user.mouse_enable_pop_stops_scroll = 1
	#enable pop click with 'control mouse' mode
    user.mouse_enable_pop_click = 1
    #When enabled, the 'Scroll Mouse' GUI will not be shown.
    user.mouse_hide_mouse_gui = 0
	#hide cursor when mouse_wake is called to enable zoom mouse
    user.mouse_wake_hides_cursor = 0
    #the amount to scroll up/down (equivalent to mouse wheel on Windows by default)
    user.mouse_wheel_down_amount = 120
	
# uncomment tag to enable mouse grid
tag(): user.mouse_grid_enabled
