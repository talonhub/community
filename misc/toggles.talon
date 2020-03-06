show command history:
	user.history_enable()
	
hide command history:
	user.history_disable()
	
welcome back: 
	user.mouse_wake()
	user.history_enable()
	
sleep all: 
	user.engine_sleep()
	user.mouse_sleep()
	user.history_disable()
