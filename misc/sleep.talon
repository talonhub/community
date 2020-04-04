mode: all
-
welcome back: 
	user.mouse_wake()
	user.history_enable()
	speech.enable()
    mode.disable('sleep')
    mode.enable('command')
    mode.disable('dictation')
	
sleep all: 
	user.history_disable()
	user.homophones_hide()
	user.help_hide()
	user.mouse_sleep()
    mode.enable('sleep')
	speech.disable()
	user.engine_sleep()
	
talon sleep: 
    mode.disable('command')
    mode.enable('dictation')

talon wake:
    mode.enable('command')
    mode.disable('dictation')
	
dragon mode:
    mode.disable('command')
    mode.enable('dictation')
	
talon mode:
	#mimic('go to sleep')
    mode.enable('command')
    mode.disable('dictation')
