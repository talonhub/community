zoom in [<number>]: 
	numb  = number or 1	
	edit.zoom_in()
	repeat(numb - 1)	
zoom out [<number>]: 
	numb  = number or 1	
	edit.zoom_out()
	repeat(numb - 1)
copy take: edit.copy()
snip take: edit.cut()
pace: edit.paste()
nope [<number>]: 
	numb  = number or 1
	edit.undo()
	repeat(numb - 1)
again [<number>]: 
	numb  = number or 1
	edit.redo()
	repeat(numb - 1)
paste match: edit.paste_match_style()
disc: edit.save()
#wipe: key(backspace)    
#(pad | padding): 
#	insert("  ") 
#	key(left)
slap: edit.line_insert_down()

