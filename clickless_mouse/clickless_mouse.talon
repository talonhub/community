-
settings():
    # size of the options
    user.clickless_mouse_radius = 25
    # the time required to dwell on an option before its triggered
    user.clickless_mouse_dwell_time = .5
    # the time the mouse must be idle before the options display
    user.clickless_mouse_idle_time_before_display = .35
    # toggle autohide hide. if <= 0, an "x" appears to exit the options.
    # otherwise, ka (keep alive) appears and the options auto hide
    user.clickless_mouse_auto_hide = 0
    # after X seconds, auto hide the options when autohide is enabled
    user.clickless_mouse_auto_hide_time = 1.0
    # when auto hide is active, option to prevent redisplay for minor motions
    user.clickless_mouse_prevent_redisplay_for_minor_motions = 0

^click less mouse$: user.clickless_mouse_toggle()