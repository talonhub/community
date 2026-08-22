tag: terminal
-

# This file contains tmux commands that are typed into the shell.
# They should be available in any terminal, not just one that's already running a tmux session.

mux: "tmux "

mux new session: insert("tmux new ")
mux kill session: insert("tmux kill-session -t ")
