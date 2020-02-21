control mouse: 
	user.knausj_talon.actions.mouse.toggle_control_mouse()
zoom mouse: 
	user.knausj_talon.actions.mouse.toggle_zoom_mouse()
camera overlay: 
	eye_mouse.camera_overlay.toggle()
(click | chiff): 
	mouse_click()
run calibration: 
	user.knausj_talon.actions.mouse.calibrate()
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
	user.knausj_talon.actions.mouse.show_cursor()
curse no: 
	user.knausj_talon.actions.mouse.hide_cursor() 
