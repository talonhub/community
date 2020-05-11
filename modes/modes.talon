#defines the various mode commands 
mode: all
-
welcome back: 
	user.mouse_wake()
	user.history_enable()
	speech.enable()
sleep all: 
	user.switcher_hide_running()
	user.history_disable()
	user.homophones_hide()
	user.help_hide()
	user.mouse_sleep()
	speech.disable()
	user.engine_sleep()
talon sleep: speech.disable()
talon wake: speech.enable()
dragon mode: speech.disable()
talon mode: speech.enable()
^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")