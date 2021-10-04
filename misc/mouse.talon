control mouse: user.mouse_toggle_control_mouse()
zoom mouse: user.mouse_toggle_zoom_mouse()
camera overlay: user.mouse_toggle_camera_overlay()
run calibration: user.mouse_calibrate()	
kick: 
	mouse_click(0)
	# close the mouse grid if open
	user.grid_close()
    	# End any open drags
	# Touch automatically ends left drags so this is for right drags specifically
	user.mouse_drag_end()

<<<<<<< HEAD
psychic: 
=======
righty:
>>>>>>> master
	mouse_click(1)
	# close the mouse grid if open
	user.grid_close()

dubclick: 
	mouse_click()
	mouse_click()
	# close the mouse grid
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
<user.modifiers> kick: 
	key("{modifiers}:down")
	mouse_click(0)
	key("{modifiers}:up")
	# close the mouse grid
	user.grid_close()
<user.modifiers> psychic: 
	key("{modifiers}:down")
	mouse_click(1)
	key("{modifiers}:up")
	# close the mouse grid
	user.grid_close()
(tripclick | triplick): 
	mouse_click()
	mouse_click()
	mouse_click()
	# close the mouse grid
	user.grid_close()
left drag | drag:
	user.mouse_drag(0)
	# close the mouse grid
	user.grid_close()

dropping: user.mouse_scroll_down_continuous()
rising: user.mouse_scroll_up_continuous()
wheel stop: user.mouse_scroll_stop()

drop: user.mouse_scroll_down()
drop tiny: mouse_scroll(20)
rise: user.mouse_scroll_up()
rise tiny: mouse_scroll(-20)
track left: mouse_scroll(0, -40)
track left tiny: mouse_scroll(0, -20)
track right: mouse_scroll(0, 40)
track right tiny: mouse_scroll(0, 20)

curse yes: user.mouse_show_cursor()
curse no: user.mouse_hide_cursor()
copy mouse position: user.copy_mouse_position()

#wheel down here:
#    user.mouse_move_center_active_window()
#    user.mouse_scroll_down()

#wheel downer here:
#    user.mouse_move_center_active_window()
#    user.mouse_scroll_down_continuous()

#wheel up here:
# 	 user.mouse_scroll_up()

#wheel tiny up here:
#    user.mouse_move_center_active_window()
#    mouse_scroll(-20)

#wheel upper here:
#    user.mouse_move_center_active_window()
#    user.mouse_scroll_up_continuous()

wheel gaze: user.mouse_gaze_scroll()

#wheel gaze here:
#    user.mouse_move_center_active_window()
#    user.mouse_gaze_scroll()

#wheel stop here:
#    user.mouse_move_center_active_window()
#    user.mouse_scroll_stop()

#wheel left here:
#   user.mouse_move_center_active_window()
#   mouse_scroll(0, -40)

#wheel tiny left here:
#   user.mouse_move_center_active_window()
#   mouse_scroll(0, -20)

#wheel right here:
#    user.mouse_move_center_active_window()
#    mouse_scroll(0, 40)

#wheel tiny right here:
#    user.mouse_move_center_active_window()
#    mouse_scroll(0, 20)
