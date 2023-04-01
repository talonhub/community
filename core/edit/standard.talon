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
(nay | nope) [<number>]: 
	numb  = number or 1
	edit.undo()
	repeat(numb - 1)
again [<number>]: 
	numb  = number or 1
	edit.redo()
	repeat(numb - 1)
paste match: edit.paste_match_style()
disk: edit.save()
disk oliver: edit.save_all()
padding: user.insert_between(" ", " ")
pour [<number_small>]: 
	numb  = number or 1
	edit.line_insert_down()
	repeat(numb - 1)
drink [<number_small>]: 
	numb  = number or 1
	edit.line_insert_up()
	repeat(numb - 1)



