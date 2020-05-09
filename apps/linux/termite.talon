os: linux
app: /termite/
not win.title: /VIM/
-

# Selection mode
shell yank: key("y")
shell select: key("ctrl-shift-space")
shell insert: key("escape")
shell ([scroll]|[page]) up: key("shift-pgup")
shell [page] down: key("shift-pgdown")
shell paste: key("ctrl-shift-v")
shell copy: key("ctrl-shift-c")
visual line: key("v")
visual line mode: key("V")
