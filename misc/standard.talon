#(jay son | jason ): "json"
#(http | htp): "http"
#tls: "tls"
#M D five: "md5"
#word (regex | rejex): "regex"
#word queue: "queue"
#word eye: "eye"
#word iter: "iter"
#word no: "NULL"
#word cmd: "cmd"
#word dup: "dup"
#word shell: "shell".
zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
scroll up: edit.page_up()
scroll down: edit.page_down()
copy that: edit.copy()
cut that: edit.cut()
pace that: edit.paste()
show clip: key(cmd-shift-v)
(undo that | nope): edit.undo()
(redo that | yes indeed): edit.redo()
paste match: edit.paste_match_style()
file save: edit.save()
padding:
	insert("  ") 
	key(left)
clapper:
	edit.line_end()
	key(enter)
clap up:
	edit.line_start()
	edit.line_start()
	key(left)
	key(enter)

slow mode: mode.enable("user.slow")

emoji hunt [<user.text>]:
	key(cmd-ctrl-space)
	sleep(100ms)
	insert(user.text or "")

^dictate <user.text>$:
    auto_insert(text)
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
    mode.disable("user.gdb")