-
settings():
    # The update frequency used when moving a window continuously
    user.win_move_frequency = "60ms"

    # The target speed, in cm/sec, for continuous move operations
    user.win_continuous_move_rate = 4.1

    # When enabled, the 'Move/Resize Window' GUI will not be shown for continuous move operations
    user.win_hide_move_gui = 0

    # The update frequency used when resizing a window continuously
    # note: setting this value too low may result in 
    user.win_resize_frequency = "60ms"

    # The target speed, in cm/sec, for continuous resize operations
    user.win_continuous_resize_rate = 4.5

    # When enabled, the 'Move/Resize Window' GUI will not be shown for continuous resize operations
    user.win_hide_resize_gui = 0

    # How long to wait (in seconds) for talon to signal completion of window move/resize requests
    user.win_set_queue_timeout = 0.2

    # How many times to retry a timed out talon window move/resize request
    user.win_set_retries = 1

    # Whether to generate warnings for anomalous events.
    user.win_verbose_warnings = 0
