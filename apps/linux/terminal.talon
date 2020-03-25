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
  key("alt-{number}")
run last:
  key(up)
  key(enter)
rerun <phrase>:
  key(ctrl-r)
  insert(phrase)
rerun search:
  key(ctrl-r)
kill all:
  key(ctrl-c)
action(edit.find):
  key(ctrl-shift-f)
action(edit.page_down):
  key(shift-pagedown)
action(edit.page_up):
  key(shift-pageup)
action(edit.paste):
  key(ctrl-shift-v)
action(edit.copy):
  key(ctrl-shift-c)
action(edit.word_left):
  key(ctrl-w-left)
action(edit.word_right):
  key(ctrl-w-right)