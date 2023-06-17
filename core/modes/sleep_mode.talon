mode: sleep
-
settings():
    #stop continuous scroll/gaze scroll with a pop
    user.mouse_enable_pop_stops_scroll = 0
    #enable pop click with 'control mouse' mode
    user.mouse_enable_pop_click = 0

# Define the commands that wake Talon.

# Note: these have repeaters on them (+) to work around the issue where, in sleep mode,
# you can run into a loop where you never hit the speech timeout, even if (because)
# you're saying the wake commands multiple times.
^(welcome back)+$:
    user.mouse_wake()
    user.history_enable()
    user.talon_mode()

^(talon wake)+$: speech.enable()
