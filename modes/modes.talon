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
talon sleep:
    speech.disable()
    user.system_command('notify-send.sh -t 3000 -f -u low "Talon Sleep"')
talon wake:
    speech.enable()
    user.system_command('notify-send.sh -t 3000 -f -u low "Talon Awake"')
dragon mode: speech.disable()
talon mode: speech.enable()
^(dictation mode|dictate)$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")
[enable] debug mode:
    mode.enable("user.gdb")
disable debug mode:
    mode.disable("user.gdb")

^force see sharp$: user.code_set_language_mode("csharp")
^force see plus plus$: user.code_set_language_mode("cplusplus")
^force python$: user.code_set_language_mode("python")
^force go (lang|language)$: user.code_set_language_mode("go")
^force (talon | talent) language$: user.code_set_language_mode("talon")
^force markdown$: user.code_set_language_mode("markdown")
^clear language modes$: user.code_clear_language_mode()
