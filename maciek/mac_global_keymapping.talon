os: mac
-

###############################################################################
### KeyPad
###############################################################################
key(keypad_1):
    key("ctrl-1") 
    user.switcher_focus_and_wait("google chrome")
key(keypad_2):
    key("ctrl-2") 
    user.switcher_focus_and_wait("code", 0.5)
key(keypad_3):
    key("ctrl-3") 
    user.switcher_focus_and_wait("kitty", 0.5)
    # When the key is post for a longer time the action is not repeated.
# key(keypad_plus:up):    key("pageup")
key(cmd-ctrl-alt-shift-p:repeat): key("pageup")
key(keypad_enter):    key("pagedown")
key(keypad_enter:repeat):    key("pagedown")
key(keypad_4): key(cmd-`)    
key(cmd-ctrl-alt-shift-z):user.go_back()
# key(keypad_5):
#     user.engine_sleep()
#     key(cmd-shift-alt-\)
# there is a mapping in karabiner configuration for this
key(f13):core.repeat_command(1)

key(ctrl-f):
    key(cmd-alt-shift-f1)
