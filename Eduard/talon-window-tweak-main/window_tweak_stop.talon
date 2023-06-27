# these commands are enabled via the tag below whenever a continuous window move/resize is running
tag: user.window_tweak_running
-

# WIP - could later add more commands here, e.g. 'pause', 'continue', 'cancel', 'faster', 'slower'
# WIP - 'cancel' would both stop and revert in one operation
# WIP - could add directional commands here to affect the window move/resize in mid flight.

# could define this 'stop' command in a separate mode...entered by the
# move_start()/resize_start() code and containing just the 'stop' command which, when
# executed, would then restore the original mode after stopping the move/resize operation.

window stop:
    user.win_stop()