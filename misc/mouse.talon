control mouse: 
	user.actions.mouse.toggle_control_mouse()
zoom mouse: 
	user.actions.mouse.toggle_zoom_mouse()
camera overlay: 
	eye_mouse.camera_overlay.toggle()
(click | chiff): 
	mouse_click()
run calibration: 
	user.actions.mouse.calibrate()
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
	user.actions.mouse.show_cursor()
curse no: 
	user.actions.mouse.hide_cursor() 
