os: linux
tag: tmux
-
tag(): splits
mux: "tmux "

#session management
mux new session: 'tmux new '
mux sessions:
    key(ctrl-b)
    key(s)
mux name session:
    key(ctrl-b)
    key($)
mux kill session: 'tmux kill-session -t'
#window management
mux new window:
    key(ctrl-b)
    key(c)
mux window <number>:
    key(ctrl-b )
    key('{number}')
mux previous window:
    key(ctrl-b)
    key(p)
mux next window:
    key(ctrl-b)
    key(n)
mux rename window:
    key(ctrl-b)
    key(,)
mux close window:
    key(ctrl-b)
    key(&)
mux split horizontal: user.split_window_horizontally()
action(user.split_window_horizontally):
    key(ctrl-b)
    key(%)
mux split vertical: user.split_window_vertically()
action(user.split_window_vertically):
    key(ctrl-b)
    key(")
mux next pane: user.split_next()
action(user.split_next):
    key(ctrl-b)
    key(o)
mux move <user.arrow>:
    key(ctrl-b)
    key(arrow)
mux close pane: user.split_clear()
action(user.split_clear):
    key(ctrl-b)
    key(x)
mux pane <number>: user.split_number(number)
