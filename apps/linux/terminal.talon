os: linux
app: /.*terminal/
-
action(app.tab_open):
  key(ctrl-shift-t)
action(app.tab_close):
  key(ctrl-shift-w)
action(app.tab_next):
  key(ctrl-pagedown)
action(app.tab_previous):
  key(ctrl-pageup)
action(app.window_open):
  key(ctrl-shift-n)
go tab <number>:
  user.keys_modifier_key("alt", number)
run last:
  key(up)
  key(enter)
kill all:
  key(ctrl-c)
action(edit.page_down):
  key(shift-pagedown)
action(edit.page_up):
  key(shift-pageup)
action(edit.paste):
  key(ctrl-shift-v)
action(edit.copy):
  key(ctrl-shift-c)