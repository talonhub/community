control mouse: 
	user.mouse_toggle_control_mouse()
zoom mouse: 
	user.mouse_toggle_zoom_mouse()
camera overlay: 
	eye_mouse.camera_overlay.toggle()
chiff: 
	mouse_click()
run calibration: 
	user.mouse_calibrate()
(righty | rickle): 
	mouse_click(1)
(dubclick | duke): 
	mouse_click()
	mouse_click()
(tripclick | triplick): 
	mouse_click()
	mouse_click()
	mouse_click()
curse yes: 
	user.mouse_show_cursor()
curse no: 
	user.mouse_hide_cursor()
drag: 
	user.mouse_drag()