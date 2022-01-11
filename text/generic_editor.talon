my email:
  "alexrkoch@gmail.com"

my phone:
  "919-749-3667"

my name:
  "Alex Koch"

portfolio site:
  "alexrkoch-portfolio-2.com"

civic crumb:
  "CiviCRM"

timer (start | stop):
    key(cmd-shift-r)

comet:
  ","

fantasizes:
  "font sizes"

fantasize:
  "font size"

shock:
  key(cmd-enter)

execute:
  key(shift-enter)

you bun to:
  "Ubuntu"

gap: 
  key(space)

slant:
  edit.line_end()
  key(enter tab)

slanter:
  edit.line_end()
  key(enter shift-tab)

slap:
  edit.line_end()
  key(enter)

zoom in: edit.zoom_in()

zoom out: edit.zoom_out()

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
    
go bottom:
    edit.file_end()
    
go top:
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

bird:
    edit.word_left()

birch:
    edit.word_right()

blitch:
    edit.extend_word_left()

blitcher:
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

