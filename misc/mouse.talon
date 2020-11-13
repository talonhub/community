control mouse: user.mouse_toggle_control_mouse()
zoom mouse: user.mouse_toggle_zoom_mouse()
camera overlay: user.mouse_toggle_camera_overlay()
run calibration: user.mouse_calibrate()	
touch: 
	mouse_click(0)
	# close the mouse grid if open
	user.grid_close()

righty: 
	mouse_click(1)
	# close the mouse grid if open
	user.grid_close()

midclick: 
	mouse_click(2)
	# close the mouse grid
	user.grid_close()

#see keys.py for modifiers.
#defaults
#command
#control
#option = alt
#shift
#super = windows key
<user.modifiers> touch: 
	key("{modifiers}:down")
	mouse_click(0)
	key("{modifiers}:up")
	# close the mouse grid
	user.grid_close()
<user.modifiers> righty: 
	key("{modifiers}:down")
	mouse_click(1)
	key("{modifiers}:up")
	# close the mouse grid
	user.grid_close()
(dubclick | duke): 
	mouse_click()
	mouse_click()
	# close the mouse grid
	user.grid_close()
(tripclick | triplick): 
	mouse_click()
	mouse_click()
	mouse_click()
	# close the mouse grid
	user.grid_close()
drag: 
	user.mouse_drag()
	# close the mouse grid
	user.grid_close()
wheel down: user.mouse_scroll_down()
wheel down here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_down()
wheel tiny [down]: mouse_scroll(20)
wheel tiny [down] here:
    user.mouse_move_center_active_window()
    mouse_scroll(20)
wheel downer: user.mouse_scroll_down_continuous()
wheel downer here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_down_continuous()
wheel up: user.mouse_scroll_up()
wheel up here:
 user.mouse_scroll_up()
wheel tiny up: mouse_scroll(-20)
wheel tiny up here:
    user.mouse_move_center_active_window()
    mouse_scroll(-20)
wheel upper: user.mouse_scroll_up_continuous()
wheel upper here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_up_continuous()
wheel gaze: user.mouse_gaze_scroll()
wheel gaze here:
    user.mouse_move_center_active_window()
    user.mouse_gaze_scroll()
wheel stop: user.mouse_scroll_stop()
wheel stop here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_stop()
wheel left: mouse_scroll(0, -40)
wheel left here:
    user.mouse_move_center_active_window()
    mouse_scroll(0, -40)
wheel tiny left: mouse_scroll(0, -20)
wheel tiny left here:
    user.mouse_move_center_active_window()
    mouse_scroll(0, -20)
wheel right: mouse_scroll(0, 40)
wheel right here:
    user.mouse_move_center_active_window()
    mouse_scroll(0, 40)
wheel tiny right: mouse_scroll(0, 20)
wheel tiny right here:
    user.mouse_move_center_active_window()
    mouse_scroll(0, 20)
curse yes: user.mouse_show_cursor()
curse no: user.mouse_hide_cursor()
copy mouse position: user.copy_mouse_position()