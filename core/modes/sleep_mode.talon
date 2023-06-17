mode: sleep
-
settings():
    #stop continuous scroll/gaze scroll with a pop
    user.mouse_enable_pop_stops_scroll = 0
    #enable pop click with 'control mouse' mode
    user.mouse_enable_pop_click = 0

#defines the commands that sleep/wake Talon

^(welcome back)+$:
    user.mouse_wake()
    user.history_enable()
    user.talon_mode()

^(talon wake)+$: speech.enable()
