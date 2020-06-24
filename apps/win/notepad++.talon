app: Notepad++ : a free (GNU) source code editor
app: notepad++.exe
-
tag(): tabs
tag(): line_commands
action(app.tab_previous):
	key(ctrl-pageup)
action(app.tab_next):
	key(ctrl-pagedown)
action(user.ide_toggle_comment):
	key(ctrl-q)