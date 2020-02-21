talon sleep: 
	speech.disable()
	
talon wake: 
	speech.enable()

#note this is only valid on Mac
dragon mode: 
    speech.disable()
    user.knausj_talon.code.engine.wake()
	
#note this is only valid on Mac
talon mode: 
	speech.enable()
    user.knausj_talon.code.engine.sleep()
	
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
