key(cmd-shift-alt-ctrl-x):
  speech.disable()

key(cmd-shift-alt-ctrl-y):
  speech.enable()

key(cmd-shift-alt-ctrl-z:down):
  user.speech_toggle()

key(cmd-shift-alt-ctrl-z:up):
  user.speech_toggle()

key(cmd-shift-alt-ctrl-f):
  user.switcher_focus_or_launch("Firefox")

key(cmd-shift-alt-ctrl-c):
  user.switcher_focus_or_launch("Cursor")

key(cmd-shift-alt-ctrl-m):
  user.switcher_focus_or_launch("Spotify")

key(cmd-shift-alt-ctrl-s):
  user.switcher_focus_or_launch("Slack")

key(cmd-shift-alt-ctrl-t):
  user.switcher_focus_or_launch("iTerm2")

key(cmd-shift-alt-ctrl-p):
  user.switcher_focus_or_launch("Postico")

key(cmd-shift-alt-ctrl-d):
  user.switcher_focus_or_launch("Discord")
