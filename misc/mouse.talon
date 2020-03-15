control mouse: 
	user.mouse_toggle_control_mouse()

zoom mouse: 
	user.mouse_toggle_zoom_mouse()
	
camera overlay: 
	eye_mouse.camera_overlay.toggle()
	
run calibration: 
	user.mouse_calibrate()
	
<user.mouse_index>: 
	mouse_click(mouse_index)
	
<user.modifiers> <user.mouse_index>: 
	key("{modifiers}:down")
	mouse_click(mouse_index)
	key("{modifiers}:up")
	
(dubclick | duke): 
	mouse_click()
	mouse_click()

(tripclick | triplick): 
	mouse_click()
	mouse_click()
	mouse_click()

scroll up: mouse_scroll(-120)
wheel tiny [down]: mouse_scroll(20)
downer: user.mouse_scroll_down_continuous()

wheel up: user.mouse_scroll_up()
wheel tiny up: mouse_scroll(-20)
supper: user.mouse_scroll_up_continuous()

gaze wheel: user.mouse_gaze_scroll()
wheel stop: user.mouse_scroll_stop()

curse yes: 
	user.mouse_show_cursor()
	
curse no: 
	user.mouse_hide_cursor()

drag: 
	user.mouse_drag()