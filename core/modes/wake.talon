#defines the commands that sleep/wake Talon
mode: sleep
-
^(welcome back)+$:
    user.mouse_wake()
    user.history_enable()
    user.talon_mode()

^(talon wake)+$: speech.enable()
