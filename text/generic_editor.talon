# Added new functionality (merge test)

slant: 
  key(enter tab)

slanter:
  key(enter shift-tab)

zoom in: edit.zoom_in()

zoom out: edit.zoom_out()

page up: key(pgup)

page down: key(pgdown)

copy: edit.copy()

slice: edit.cut()

spark: edit.paste()

undo: edit.undo()

redo: edit.redo()

file save: edit.save() 

tell sink:
	edit.line_end()
	insert(";")
	key(enter) 

enter:
    key(enter)

bird:
    edit.word_left()

birch:
    edit.word_right()

go left:
    edit.left()

go right:
    edit.right()

go up:
    edit.up()

go down:
    edit.down()

go end:
    edit.line_end()

go home:
    edit.line_start()

go way end:
    edit.file_end()
    edit.line_end()

go way home:
    edit.file_start()

page down:
    edit.page_down()

page up:
    edit.page_up()

# selecting
shackle:
    edit.select_line()

select all:
    edit.select_all()

select left:
    edit.extend_left()

select right:
    edit.extend_right()

select up:
    edit.extend_line_up()

select down:
    edit.extend_line_down()

select word:
    edit.select_word()

blitch:
    edit.extend_word_left()

rich:
    edit.extend_word_right()

select home:
    edit.extend_line_start()

select end:
    edit.extend_line_end()

select way home:
    edit.extend_file_start()

select way end:
    edit.extend_file_end()

# editing
indent [more]:
    edit.indent_more()

(indent less | out dent):
    edit.indent_less()

# deleting
clear line:
    edit.delete_line()

junk:
    key(backspace)

tabby:
    key(tab)

deli:
    key(delete)

clear up:
    edit.extend_line_up()
    edit.delete()

clear down:
    edit.extend_line_down()
    edit.delete()

clear word:
    edit.delete_word()

clear word left:
    edit.extend_word_left()
    edit.delete()

clear word right:
    edit.extend_word_right()
    edit.delete()

clear way left:
    edit.extend_line_start()
    edit.delete()

clear way right:
    edit.extend_line_end()
    edit.delete()

clear way up:
    edit.extend_file_start()
    edit.delete()

clear way down:
    edit.extend_file_end()
    edit.delete()

#copy commands
copy all:
    edit.select_all()
    edit.copy()
#to do: do we want these variants, seem to conflict
# copy left:
#      edit.extend_left()
#      edit.copy()
# copy right:
#     edit.extend_right()
#     edit.copy()
# copy up:
#     edit.extend_up()
#     edit.copy()
# copy down:
#     edit.extend_down()
#     edit.copy()

copy word:
    edit.select_word()
    edit.copy()

copy word left:
    edit.extend_word_left()
    edit.copy()

copy word right:
    edit.extend_word_right()
    edit.copy()

copy line:
    edit.select_line()
    edit.copy()

#cut commands
cut everything:
    edit.select_all()
    edit.cut()
#to do: do we want these variants
# cut left:
#      edit.select_all()
#      edit.cut()
# cut right:
#      edit.select_all()
#      edit.cut()
# cut up:
#      edit.select_all()
#     edit.cut()
# cut down:
#     edit.select_all()
#     edit.cut()

cut word:
    edit.select_word()
    edit.cut()

cut word left:
    edit.extend_word_left()
    edit.cut()

cut word right:
    edit.extend_word_right()
    edit.cut()

cut line:
    edit.select_line()
    edit.cut()
