app: kitty
os: linux
-
tag(): terminal
tag(): user.git
tag(): user.tabs
tag(): user.splits

scroll line up:
  key(ctrl-shift-up)

scroll line down:
  key(ctrl-shift-down)

pinch:
  key(ctrl-shift-pageup)

punch:
  key(ctrl-shift-pagedown)

strike out:
  key(ctrl-shift-home)

struck out:
  key(ctrl-shift-end)

action(app.tab_open):
  key(ctrl-shift-t)

action(app.tab_close):
  key(ctrl-shift-q)

action(app.tab_next):
  key(ctrl-shift-right)

action(app.tab_previous):
  key(ctrl-shift-left)

tab push:
  key(ctrl-shift-.)

tab shift:
  key(ctrl-shift-,)

tab title:
  key(ctrl-shift-alt-t)

window new:
  key(ctrl-shift-n)

action(user.split_flip):
  key(ctrl-shift-l)

action(user.split_window):
  key(ctrl-shift-enter)

action(user.split_clear):
  key(ctrl-shift-w)

action(user.split_next):
  key(ctrl-shift-])

action(user.split_last):
  key(ctrl-shift-[)

action(user.split_window_right):
  key(ctrl-shift-f)

action(user.split_window_left):
  key(ctrl-shift-b)

action(user.split_number):
  key(ctrl-shvift-{number})

whack:
  key(ctrl-w)
whack all:
	key(ctrl-k)
bump:
  key(escape d)
bump all:
  key(ctrl-u)
drop:
  key(ctrl-y)
undo:
  key(ctrl-_)
last argument:
  key(alt-.)
