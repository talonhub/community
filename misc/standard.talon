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
page up: key(pgup)
page down: key(pgdown)
copy that: edit.copy()
cut that: edit.cut()
pace that: edit.paste()
show clip: key(cmd-shift-v)
(undo that | nope): edit.undo()
redo that: edit.redo()
paste match: edit.paste_match_style()
file save: edit.save()
wipe: key(backspace)    
padding: 
	insert("  ") 
	key(left)
clap it:
	edit.line_end()
	key(enter)
clap up:
	edit.line_start()
	edit.line_start()
	key(left)
	key(enter)