show command history:
	user.history_enable()
	
hide command history:
	user.history_disable()

clear command history:
	user.history_clear()

help alphabet:
	user.help_alphabet(user.get_alphabet())

help context:
	user.help_context()

help active context:
	user.help_context_enabled()

help context <user.help_contexts>: user.help_selected_context(help_contexts)

hide help:
	user.help_hide()

