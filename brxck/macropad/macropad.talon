# Layer 0

# A   @1  @2  @3
# B   C   D   E
# W   X   Y   Z


# key(cmd-shift-alt-ctrl-a):

# key(cmd-shift-alt-ctrl-b):

# key(cmd-shift-alt-ctrl-c):

key(cmd-shift-alt-ctrl-d):
  user.desktop_last()

key(cmd-shift-alt-ctrl-e):
  user.desktop_next()

key(cmd-shift-alt-ctrl-w:down):
    user.wispr_toggle_down()

key(cmd-shift-alt-ctrl-w:up):
    user.wispr_toggle_up()

key(cmd-shift-alt-ctrl-x):
  user.cancel_current_phrase()
  speech.disable()

key(cmd-shift-alt-ctrl-y): speech.enable()

key(cmd-shift-alt-ctrl-z:down):
  user.speech_toggle_down()

key(cmd-shift-alt-ctrl-z:up):
  user.speech_toggle_up()

# Layer 1

# @0   @    F13  F14
# F15  F16  F17  F18
# F19  F20  F21  F22

# key(cmd-shift-alt-ctrl-f13):
# key(cmd-shift-alt-ctrl-f14):
# key(cmd-shift-alt-ctrl-f16):
# key(cmd-shift-alt-ctrl-f17):
# key(cmd-shift-alt-ctrl-f18):
# key(cmd-shift-alt-ctrl-f19):
# key(cmd-shift-alt-ctrl-f20):

# f21+ don't seem to work
key(cmd-shift-alt-ctrl-+):
  user.raycast("Toggle System Appearance")

key(cmd-shift-alt-ctrl-_):
  speech.enable()

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
