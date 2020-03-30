mode: all
-
welcome back: 
	user.mouse_wake()
	user.history_enable()
	mode.enable('command')
	mode.disable('dictation')
	mode.disable('sleep')
	
sleep all: 
	user.history_disable()
	user.homophones_hide()
	user.help_hide()
	
	#this assums dragon
	#put dragon to sleep
	#mimic('go to sleep')
	user.engine_sleep()
	user.mouse_sleep()
	mode.enable('sleep')
	speech.disable()
	
talon sleep: 
	speech.disable()
	mode.disable('command')

talon wake:
	speech.enable()
	mode.enable('command')
	
dragon mode:
	#mimic('wake up')
	speech.disable()
	mode.disable('sleep')
    mode.disable('command')
    mode.enable('dictation')
	user.engine_wake()
	
talon mode:
	#mimic('go to sleep')
	speech.enable()
	mode.disable('sleep')
	mode.enable('command')
    mode.disable('dictation')
	user.engine_wake()
