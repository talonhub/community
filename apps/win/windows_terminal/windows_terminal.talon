app: windows_terminal
-
tag(): user.tabs
tag(): terminal

# commands that work regardless of active terminal should go here.

# windows terminal config based on mrob95's
# https://github.com/mrob95/WindowsTerminal-config/blob/master/settings.json

action(edit.paste): key(ctrl-shift-v)
action(edit.copy): key(ctrl-shift-c)
action(app.tab_close): key(ctrl-shift-w)
action(app.tab_open): key(ctrl-shift-t)

settings open : key(ctrl-,)
focus left: key(ctrl-alt-shift-left)
focus right: key(ctrl-alt-shift-right)
focus up: key(ctrl-alt-shift-up)
focus down: key(ctrl-alt-shift-down)
split right: key(ctrl-shift-h)
split down: key(ctrl-h)
term menu: key(ctrl-shift-f1)

run last: key(up enter)
kill all:
  key(ctrl-c)
  insert("y")
  key(enter)
  
