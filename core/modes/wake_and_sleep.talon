#defines the commands that sleep/wake Talon
mode: all
-
^(welcome back)+$:
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
<<<<<<< HEAD
^talon sleep [<phrase>]$:
    speech.disable()
    mode.disable("noise")
^talon wake$:
    speech.enable()
    mode.enable("noise")
=======
^talon sleep [<phrase>]$: speech.disable()
^(talon wake)+$: speech.enable()
>>>>>>> d61854d8bdfa61dc0e60e9570a8c4fcec889f00e
