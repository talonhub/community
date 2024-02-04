mode: sleep
not mode: sleep
not speech.engine: dragon
-
^talon wake [<phrase>]$: speech.enable()

# We define this *only* if the speech engine isn't Dragon, because if you're using Dragon,
# "wake up" is used to specifically control Dragon, and not affect Talon.
#
# It's a useful and well known command, though, so if you're using any other speech
# engine, this controls Talon.
^(wake up)+$: speech.enable()

# We define this *only* if the speech engine isn't Dragon, because if you're using Dragon,
# "go to sleep" is used to specifically control Dragon, and not affect Talon.
#
# It's a useful and well known command, though, so if you're using any other speech
# engine, this controls Talon.
#
# For a note about the optional <phrase>, see to_sleep_mode.talon.
^go to sleep [<phrase>]$: speech.disable()
^talon sleep [<phrase>]$: speech.disable()

^sleep all [<phrase>]$:
    user.switcher_hide_running()
    user.history_disable()
    user.homophones_hide()
    user.help_hide()
    user.mouse_sleep()
    speech.disable()
    user.engine_sleep()
