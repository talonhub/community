#defines the commands that sleep/wake Talon
mode: all
-
^welcome back$:
    user.mouse_wake()
    user.history_enable()
    user.talon_mode()
^sleep all$:
    user.switcher_hide_running()
    user.history_disable()
    user.homophones_hide()
    user.help_hide()
    user.mouse_sleep()
    speech.disable()
    user.engine_sleep()
    
^go to sleep$: speech.disable()
^drowse$: speech.disable()
^talon sleep$: speech.disable()
^dot slap$: speech.disable()
^talon wake$: speech.enable()
^wake up$: speech.enable()


