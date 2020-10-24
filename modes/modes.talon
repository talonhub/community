#defines the various mode commands
mode: all
    -
# welcome back:
    # user.mouse_wake()
    # user.history_enable()
    # speech.enable()
talon sleep all:
    user.switcher_hide_running()
    user.history_disable()
    user.homophones_hide()
    user.help_hide()
    user.mouse_sleep()
    speech.disable()
    user.engine_sleep()
    user.mouse_pop_off()



talon sleep: speech.disable()

talon awaken:
    speech.enable()
    user.mouse_pop_on()

okay talon dictation:
    speech.disable()
    key(ctrl-0)


[enable] debug mode:
    mode.enable("user.gdb")
disable debug mode:
    mode.disable("user.gdb")
^force see sharp$: user.code_set_language_mode("csharp")
^force see plus plus$: user.code_set_language_mode("cplusplus")
^force go (lang|language)$: user.code_set_language_mode("go")
^force java script$: user.code_set_language_mode("javascript")
^force type script$: user.code_set_language_mode("typescript")
^force markdown$: user.code_set_language_mode("markdown")
^force python$: user.code_set_language_mode("python")
^force talon [language]$: user.code_set_language_mode("talon")
^clear language modes$: user.code_clear_language_mode()
