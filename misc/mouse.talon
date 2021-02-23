control mouse: user.mouse_toggle_control_mouse()
zoom mouse: user.mouse_toggle_zoom_mouse()
camera overlay: user.mouse_toggle_camera_overlay()
run calibration: user.mouse_calibrate()	
touch: 
	mouse_click(0)
	# close the mouse grid if open
	user.grid_close()

right click: 
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
dubclick: 
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
(scroll | school) down: user.mouse_scroll_down()
(scroll | school) down here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_down()
(scroll | school) tiny [down]: mouse_scroll(20)
(scroll | school) tiny [down] here:
    user.mouse_move_center_active_window()
    mouse_scroll(20)
(scroll | school) downer: user.mouse_scroll_down_continuous()
(scroll | school) downer here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_down_continuous()
(scroll | school) up: user.mouse_scroll_up()
(scroll | school) up here:
 user.mouse_scroll_up()
(scroll | school) tiny up: mouse_scroll(-20)
(scroll | school) tiny up here:
    user.mouse_move_center_active_window()
    mouse_scroll(-20)
(scroll | school) upper: user.mouse_scroll_up_continuous()
(scroll | school) upper here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_up_continuous()
(scroll | school) gaze: user.mouse_gaze_scroll()
(scroll | school) gaze here:
    user.mouse_move_center_active_window()
    user.mouse_gaze_scroll()
(scroll | school) stop: user.mouse_scroll_stop()
(scroll | school) stop here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_stop()
(scroll | school) left: mouse_scroll(0, -40)
(scroll | school) left here:
    user.mouse_move_center_active_window()
    mouse_scroll(0, -40)
(scroll | school) tiny left: mouse_scroll(0, -20)
(scroll | school) tiny left here:
    user.mouse_move_center_active_window()
    mouse_scroll(0, -20)
(scroll | school) right: mouse_scroll(0, 40)
(scroll | school) right here:
    user.mouse_move_center_active_window()
    mouse_scroll(0, 40)
(scroll | school) tiny right: mouse_scroll(0, 20)
(scroll | school) tiny right here:
    user.mouse_move_center_active_window()
    mouse_scroll(0, 20)
curse yes: user.mouse_show_cursor()
curse no: user.mouse_hide_cursor()
copy mouse position: user.copy_mouse_position()