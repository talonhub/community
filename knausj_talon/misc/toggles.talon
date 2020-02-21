talon sleep: 
	speech.disable()
	
talon wake: 
	speech.enable()

#note this is only valid on Mac
dragon mode: 
    speech.disable()
    user.knausj_talon.actions.engine.wake()
	
#note this is only valid on Mac
talon mode: 
	speech.enable()
    user.knausj_talon.actions.engine.sleep()
	
show command history:
	user.knausj_talon.actions.history.enable()
	
hide command history:
	user.knausj_talon.actions.history.disable()
	
welcome back: 
	user.knausj_talon.actions.mouse.wake()
	user.knausj_talon.actions.history.enable()
	
sleep all: 
	user.knausj_talon.actions.engine.sleep()
	user.knausj_talon.actions.mouse.sleep()
	user.knausj_talon.actions.history.disable()
