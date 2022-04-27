#defines the commands that sleep/wake Talon
mode: all
-
^welcome back$:
    user.mouse_wake()
    user.history_enable()
    user.talon_mode()
^sleep all [<phrase>]$:
    user.switcher_hide_running()
    user.history_disable()
    user.homophones_hide()
    user.help_hide()
    user.mouse_sleep()
    speech.disable()
    user.engine_sleep()
    mode.disable("face")
^talon sleep [<phrase>]$: speech.disable()
^drowse [<phrase>]$: 
    speech.disable()
    user.mouse_sleep()
    mode.disable("face")
#^talon wake$: speech.enable()
^jolt$: 
    speech.enable()
