tag: user.tmux
-

mux: "tmux "

# Session management
mux new session: insert("tmux new ")
mux sessions: user.tmux_keybind("s")
mux name session: user.tmux_keybind("$")
mux kill session: insert("tmux kill-session -t ")

# Window management
mux new window: user.tmux_keybind("c")
mux window <number>: user.tmux_keybind("{number}")
mux previous window: user.tmux_keybind("p")
mux next window: user.tmux_keybind("n")
mux rename window: user.tmux_keybind(",")
mux close window: user.tmux_keybind("&")

# Pane management
mux split horizontal: user.tmux_keybind("\"")
mux split vertical: user.tmux_keybind("%")
mux next pane: user.tmux_keybind("o")
mux move <user.arrow_key>: user.tmux_keybind(arrow_key)
mux close pane: user.tmux_keybind("x")

# Say a number right after this command, to switch to pane
mux pane numbers: user.tmux_keybind("q")
