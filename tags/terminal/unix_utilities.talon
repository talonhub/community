tag: user.unix_utilities
-

core {user.unix_utility}: "{unix_utility} "

# Tmux commands that are typed into the shell.
mux: "tmux "
mux new session: insert("tmux new ")
mux kill session: insert("tmux kill-session -t ")
