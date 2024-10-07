# Layer 0

# A   @1  @2  @3
# B   C   D   E
# W   X   Y   Z


# key(cmd-shift-alt-ctrl-a):
  
# key(cmd-shift-alt-ctrl-b):

# key(cmd-shift-alt-ctrl-c):

# key(cmd-shift-alt-ctrl-d):

# key(cmd-shift-alt-ctrl-e):

key(cmd-shift-alt-ctrl-w):
  user.mode_toggle()

key(cmd-shift-alt-ctrl-x):
  speech.disable()

key(cmd-shift-alt-ctrl-y): speech.enable()

key(cmd-shift-alt-ctrl-z:down):
  user.speech_toggle_down()

key(cmd-shift-alt-ctrl-z:up):
  user.speech_toggle_up()

# Layer 1

# @0  @   3   4
# 5   6   7   8
# 9   10  11  12

# ...

# Layer 2

# @0  2   @   4
# 5   6   7   8
# 9   10  11  12

key(cmd-shift-alt-ctrl-2):
  user.switcher_focus_or_launch("Firefox")

key(cmd-shift-alt-ctrl-3): user.switcher_focus_or_launch("Firefox")

key(cmd-shift-alt-ctrl-4): user.switcher_focus_or_launch("Cursor")

key(cmd-shift-alt-ctrl-5): user.switcher_focus_or_launch("Spotify")

key(cmd-shift-alt-ctrl-6): user.switcher_focus_or_launch("Slack")

key(cmd-shift-alt-ctrl-7): user.switcher_focus_or_launch("Discord")

key(cmd-shift-alt-ctrl-8):
  user.switcher_focus_or_launch("Postico")

# Layer 3

# @0  F2  F3  @3
# F5  F6  F7  F8
# F9  F10 F11 F12
