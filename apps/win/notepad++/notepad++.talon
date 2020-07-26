app: Notepad++ : a free (GNU) source code editor
app: notepad++.exe
-
tag(): find_and_replace
tag(): line_commands
tag(): tabs
action(app.tab_previous):
	key(ctrl-pageup)
action(app.tab_next):
	key(ctrl-pagedown)
action(user.ide_toggle_comment):
	key(ctrl-q)
action(edit.line_clone):
	key(ctrl-d)
action(edit.line_swap_up):
	key(ctrl-shift-up)
action(edit.line_swap_down):
	key(ctrl-shift-down)