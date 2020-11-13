os: linux
app: Guake
-
#comment or remove tags for command sets you don't want
#quake doesn't support the file_manager stuff
#tag(): user.file_manager
tag(): user.git
tag(): user.kubectl
tag(): user.tabs
tag(): terminal

action(app.tab_open):
  key(ctrl-shift-t)
action(app.tab_close):
  key(ctrl-shift-w)
action(app.tab_next):
  key(ctrl-pagedown)
action(app.tab_previous):
  key(ctrl-pageup)
