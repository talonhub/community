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
^go to sleep$: speech.disable()
^wake up$: speech.enable()
^timer sleep$: 
  key(cmd-shift-r)
  speech.disable()
^timer wake$:
  speech.enable()  
  key(cmd-shift-r)
^time (are | or) wake$:
  speech.enable()  
  key(cmd-shift-r)

