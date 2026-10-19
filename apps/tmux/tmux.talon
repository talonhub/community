app: tmux
-

# This file contains tmux commands that only make sense within a running tmux session.

tag(): user.splits
tag(): user.tabs

# Note that you will need to add something to match the tmux app in your configuration
# This is not active by default
# Adding a file with a matcher for detecting tmux active in your terminal and activating
# the tmux tag is required
# Something like:
#
# title: /^tmux/
# -
# tag(): user.tmux

# pane management - these commands use the word split to match with the splits
# tag defined in tags/splits/splits.talon
go split <user.arrow_key>: user.tmux_keybind(arrow_key)
#Say a number after this command to switch to pane
go split: user.tmux_execute_command("display-panes -d 0")

# Session management
mux sessions: user.tmux_keybind("s")
mux name session: user.tmux_keybind("$")

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
