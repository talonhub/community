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
paste it: edit.paste()

nope: edit.undo()
redo that: edit.redo()
paste match: edit.paste_match_style()

# TODO(maciejk): at one word command, like disk but I can't use this because it conflicts with dish in my alphabet
file save: edit.save()
go$:
	key(enter)
   
  
padding: 
	insert("  ") 
	key(left)
slap:
	edit.line_end()
	key(enter)
drink line:
    edit.line_start()
    key(enter)
    key(up)