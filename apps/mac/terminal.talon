os: mac
app: Terminal
-
action(app.tab_open):
  key(cmd-t)
action(app.tab_close):
  key(cmd-w)
action(app.tab_next):
  key(ctrl-tab)
action(app.tab_previous):
  key(ctrl-shift-tab)
run last:
    key(up)
    key(enter)
kill all:
      key(ctrl-c)
action(edit.page_down):
  key(command-pagedown)
action(edit.page_up):
  key(command-pageup)