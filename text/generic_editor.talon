lorem short:
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit"

lorem long:
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."

lorem very long:
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

note up:
    key(cmd-ctrl-up)

note down:
    key(cmd-ctrl-down)

note check:
    key(shift-cmd-U)

findy:
  key(cmd-f)

shock:
  key(cmd-enter)

slant:
  edit.line_end()
  key(enter tab)

slanter:
  edit.line_end()
  key(enter shift-tab)

slappy:
  edit.line_end()
  key(enter)

(indent | push):
    key(tab)

dedent:
    key(shift-tab)

zoom in: edit.zoom_in()

zoom out: edit.zoom_out()

(copy | snippet): edit.copy()

(cut | slice): edit.cut()

(paste | spark): edit.paste()

undo: edit.undo()

redo: edit.redo()

file save: edit.save()

tell sink:
	edit.line_end()
	insert(";")
	key(enter)

stub sink:
	edit.line_end()
	insert(";")

tell comma:
	edit.line_end()
	insert(",")
	key(enter)

stub comma:
	edit.line_end()
	insert(",")

return:
    key(enter)

(go left | west):
    edit.left()

(go right | east):
    edit.right()

(go up | north):
    edit.up()

(go down | south):
    edit.down()

line end:
    edit.line_end()

line start:
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

select line start:
    edit.extend_line_start()

select line end:
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
deli line:
    edit.delete_line()

junk:
    key(backspace)

deli:
    key(delete)

deli up:
    edit.extend_line_up()
    edit.delete()

deli down:
    edit.extend_line_down()
    edit.delete()

spark word:
    edit.select_word()
    edit.paste()

spark line:
    edit.select_line()
    edit.paste()

deli word:
    edit.delete_word()

deli word left:
    edit.extend_word_left()
    edit.delete()

deli word right:
    edit.extend_word_right()
    edit.delete()

deli way left:
    edit.extend_line_start()
    edit.delete()

deli way right:
    edit.extend_line_end()
    edit.delete()

deli way up:
    edit.extend_file_start()
    edit.delete()

deli way down:
    edit.extend_file_end()
    edit.delete()

#copy commands
snippet all:
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

snippet word:
    edit.select_word()
    edit.copy()

snippet word left:
    edit.extend_word_left()
    edit.copy()

snippet word right:
    edit.extend_word_right()
    edit.copy()

snippet line:
    edit.select_line()
    edit.copy()

#cut commands
slice everything:
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

slice word:
    edit.select_word()
    edit.cut()

slice word left:
    edit.extend_word_left()
    edit.cut()

slice word right:
    edit.extend_word_right()
    edit.cut()

slice line:
    edit.select_line()
    edit.cut()
