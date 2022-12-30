find it: edit.find()

next one: edit.find_next()

go word left: edit.word_left()

go word right: edit.word_right()

go left: edit.left()

go right: edit.right()

go up: edit.up()

go down: edit.down()

go line start: edit.line_start()

go line end: edit.line_end()

go way left:
    edit.line_start()
    edit.line_start()

go way right: edit.line_end()

go way down: edit.file_end()

go way up: edit.file_start()

go bottom: edit.file_end()

go top: edit.file_start()

go page down: edit.page_down()

go page up: edit.page_up()

# selecting
select line: edit.select_line()

select all: edit.select_all()

select left: edit.extend_left()

select right: edit.extend_right()

select up: edit.extend_line_up()

select down: edit.extend_line_down()

select word: edit.select_word()

select word left: edit.extend_word_left()

select word right: edit.extend_word_right()

select way left: edit.extend_line_start()

select way right: edit.extend_line_end()

select way up: edit.extend_file_start()

select way down: edit.extend_file_end()

# editing
indent [more]: edit.indent_more()

(indent less | out dent): edit.indent_less()

# deleting
clear line: edit.delete_line()

clear left: key(backspace)

clear right: key(delete)

clear up:
    edit.extend_line_up()
    edit.delete()

clear down:
    edit.extend_line_down()
    edit.delete()

clear word: edit.delete_word()

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

clear all:
    edit.select_all()
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

copy word left: user.copy_word_left()

copy word right: user.copy_word_right()

copy line:
    edit.select_line()
    edit.copy()

#cut commands
cut all:
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

cut word left: user.cut_word_left()

cut word right: user.cut_word_right()

cut line: user.cut_line()

(pace | paste) all:
    edit.select_all()
    edit.paste()

# duplication
clone that: edit.selection_clone()
clone line: edit.line_clone()
