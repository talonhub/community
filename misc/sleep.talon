mode: all
-
welcome back: 
	user.mouse_wake()
	user.history_enable()
	speech.enable()	
sleep all: 
	user.history_disable()
	user.homophones_hide()
	user.help_hide()
	user.mouse_sleep()
	speech.disable()
	user.engine_sleep()
    mode.disable('dictation')
talon sleep: speech.disable()
talon wake: speech.enable()
dragon mode: speech.disable()
talon mode: speech.enable()