mode: sleep
not tag: user.deep_sleep
-

^(welcome back)+$:
    user.mouse_wake()
    user.history_enable()
    user.talon_mode()
