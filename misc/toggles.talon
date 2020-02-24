show command history:
	user.knausj_talon.code.history.enable()
	
hide command history:
	user.knausj_talon.code.history.disable()
	
welcome back: 
	user.knausj_talon.code.mouse.wake()
	user.knausj_talon.code.history.enable()
	
sleep all: 
	user.knausj_talon.code.engine.sleep()
	user.knausj_talon.code.mouse.sleep()
	user.knausj_talon.code.history.disable()
