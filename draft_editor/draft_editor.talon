user.draft_editor_running: True
not app: draft_editor
-

draft this:
	user.draft_editor_open()

draft all:
	edit.select_all()
	user.draft_editor_open()

draft line:
	edit.select_line()
	user.draft_editor_open()