control mouse: 
	user.knausj_talon.code.mouse.toggle_control_mouse()
zoom mouse: 
	user.knausj_talon.code.mouse.toggle_zoom_mouse()
camera overlay: 
	eye_mouse.camera_overlay.toggle()
(click | chiff): 
	mouse_click()
run calibration: 
	user.knausj_talon.code.mouse.calibrate()
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
	user.knausj_talon.code.mouse.show_cursor()
curse no: 
	user.knausj_talon.code.mouse.hide_cursor() 
