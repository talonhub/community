mode: sleep
-
settings():
    # Stop continuous scroll/gaze scroll with a pop
    user.mouse_enable_pop_stops_scroll = 0
    # Enable pop click with 'control mouse' mode
    user.mouse_enable_pop_click = 0
    # Stop mouse scroll down using hiss noise
    user.mouse_enable_hiss_scroll = 0
    # Enable pop wake. Note that if this is enabled, it will disable popping to click in sleep mode, if you set `mouse_enable_pop_wake = 2`.
    user.mouse_enable_pop_wake = 0
