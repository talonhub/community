show command history:
	user.history_enable()
	
hide command history:
	user.history_disable()
	
welcome back: 
	user.mouse_wake()
	user.history_enable()

sleep all: 
	user.history_disable()
	user.homophones_hide()
	user.help_hide()
	user.engine_sleep()
	user.mouse_sleep()

help alphabet:
	user.help_alphabet(user.get_alphabet())

help context:
	user.help_context()

help active context:
	user.help_context_enabled()

hide help:
	user.help_hide()