# go left, go left left down, go 5 left 2 down
# go word left, go 2 words right
go <user.navigation_step>+: user.perform_navigation_steps(navigation_step_list)
    
# Compound of action(select, clear, copy, cut, paste, etc.) and modifier(word, line, etc.) commands for editing text.
# eg: "select line", "clear all"
<user.edit_action> <user.edit_modifier>: user.edit_command(edit_action, edit_modifier)

zoom in [<number_small>]: 
	numb  = number_small or 1	
	edit.zoom_in()
	repeat(numb - 1)	
zoom out [<number_small>]: 
	numb  = number_small or 1	
	edit.zoom_out()
	repeat(numb - 1)
zoom reset:
    edit.zoom_reset()

copy: edit.copy()
slice: edit.cut()

pace: edit.paste()
(nay | nope) [<number_small>]: 
	numb = number or 1
	edit.undo()
	repeat(numb - 1)
again [<number_small>]: 
	numb  = number_small or 1
	edit.redo()
	repeat(numb - 1)
paste match: edit.paste_match_style()
disk: edit.save()
disk oliver: edit.save_all()
padding: user.insert_between(" ", " ")
pour [<number_small>]: 
	numb  = number_small or 1
	edit.line_insert_down()
	repeat(numb - 1)
drink [<number_small>]: 
	numb  = number_small or 1
	edit.line_insert_up()
	repeat(numb - 1)
spring:
    edit.word_right()
spring <number_small>:
    edit.word_right()
    repeat(number_small-1)
draw:
    edit.word_left()
draw <number_small>:
    edit.word_left()
    repeat(number_small-1)

wipe <number_small>: 
    edit.delete()
    repeat(number_small-1)
wiper:
    edit.extend_line_start()
    edit.delete()
drill <number_small>: 
    edit.delete()
    repeat(number_small-1)
(drill) tail:
    edit.extend_line_end()
    edit.delete()
(drill) head: 
    edit.extend_line_start()
    edit.delete()
driller: 
    edit.extend_line_end()
    edit.delete()  
tail:
    edit.line_end()
head:
    edit.line_start()

far left:
    edit.line_start()
    edit.line_start()

far right:
    edit.line_end()

far down:
    edit.file_end()

far up:
    edit.file_start()

# go page down:
#     edit.page_down()

# go page up:
#     edit.page_up()
take left [<number_small>]:
    numb = number_small or 1
    edit.extend_left()
    repeat(numb - 1)

take right [<number_small>]:
    numb = number_small or 1
    edit.extend_right()
    repeat(numb - 1)

take up [<number_small>]:
    numb = number_small or 1
    edit.extend_line_up()
    repeat(numb - 1)

take down [<number_small>]:
    numb = number_small or 1
    edit.extend_line_down()
    repeat(numb - 1)
    
take draw [<number_small>]:
    numb = number_small or 1
    edit.extend_word_left()
    repeat(numb - 1)

take spring [<number_small>]:
    numb = number_small or 1
    edit.extend_word_right()
    repeat(numb - 1)

take far up:
    edit.extend_file_start()

take far down:
    edit.extend_file_end()

# editing
tabby:
    edit.indent_more()
tabby <number_small>:
    edit.indent_more()
    repeat(number_small-1)

retabby [<number_small>]:
    numb = number_small or 1
    edit.indent_less()
    repeat(numb-1)

# deleting
wipe (line | row) [<number_small>]:
    numb = number_small or 1
    edit.delete_line()
    repeat(numb-1)
    
wipe up [<number_small>]:
    numb = number_small or 1
    edit.extend_line_up()
    repeat(numb-1)
    edit.delete()
    
wipe down [<number_small>]:
    numb = number_small or 1
    edit.extend_line_down()
    repeat(numb-1)
    edit.delete()
    
wipe word [<number_small>]:
    numb = number_small or 1
    edit.delete_word()
    repeat(numb-1)
    
wipe draw [<number_small>]:
    numb = number_small or 1
    edit.extend_word_left()
    repeat(number_small-1)
    edit.delete()
    
wipe spring [<number_small>]:
    numb = number_small or 1
    edit.extend_word_right()
    repeat(number_small-1)

wipe far up:
    edit.extend_file_start()
    edit.delete()
    
wipe far down:
    edit.extend_file_end()
    edit.delete()
    
copy draw [<number_small>]:
    numb = number_small or 1
    edit.extend_word_left()
    repeat(number_small-1)
    edit.copy()
    
copy spring [<number_small>]:
    numb = number_small or 1
    edit.extend_word_right()
    repeat(number_small-1)
    edit.copy()
    
copy line:
    edit.select_line()
    edit.copy()
    
copy far left:
    edit.extend_line_start()
    edit.delete()
    
copy far right:
    edit.extend_line_end()
    edit.copy()
    
copy far up:
    edit.extend_file_start()
    edit.copy()
    
copy far down:
    edit.extend_file_end()
    edit.copy()
    
slice draw [<number_small>]:
    numb = number_small or 1
    edit.extend_word_left()
    repeat(numb - 1)
    edit.cut()
    
slice spring [<number_small>]:
    numb = number_small or 1
    edit.extend_word_right()
    repeat(numb - 1)
    edit.cut()

# duplication
clone that: edit.selection_clone()
clone line: edit.line_clone()


