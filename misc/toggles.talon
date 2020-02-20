talon sleep: 
	speech.disable()
	
talon wake: 
	speech.enable()

#note this is only valid on Mac
dragon mode: 
    speech.disable()
    user.actions.engine.wake()
	
#note this is only valid on Mac
talon mode: 
	speech.enable()
    user.actions.engine.sleep()
	
show command history:
	user.actions.canvas_history.enable()
	
hide command history:
	user.actions.canvas_history.disable()
	
welcome back: 
	user.actions.mouse.wake()
	user.actions.canvas_history.enable()
	
sleep all: 
	user.actions.engine.sleep()
	user.actions.mouse.sleep()
	user.actions.canvas_history.disable()
