mode: sleep
-
settings():
    #stop continuous scroll/gaze scroll with a pop
    user.mouse_enable_pop_stops_scroll = 0
	#enable pop click with 'control mouse' mode
	user.mouse_enable_pop_click = 0
    #so that postalveolar click doesn't inadvertantly trigger a command
    speech.timeout = 0.01
#this exists solely to prevent talon from walking up super easily in sleep mode at the moment with wav2letter
<phrase>: skip()

action(user.postalveolar_click):
    user.mouse_wake()
    user.history_enable()
    user.talon_mode()
