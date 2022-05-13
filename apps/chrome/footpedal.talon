app: chrome
os: mac
-
# right pedal down
key(cmd-ctrl-shift-r): 
    user.mouse_scroll_up_continuous()
    user.mouse_scroll_up_continuous()
# right pedal up
key(cmd-ctrl-shift-alt-r):
    user.mouse_scroll_stop() 
# left pedal down
key(cmd-ctrl-shift-l): 
    user.mouse_scroll_down_continuous()
    user.mouse_scroll_down_continuous()
# left pedal up
key(cmd-ctrl-shift-alt-l): 
    user.mouse_scroll_stop()
