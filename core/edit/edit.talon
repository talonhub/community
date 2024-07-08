# Zoom
zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
zoom reset: edit.zoom_reset()

# Searching
find it: edit.find()
next one: edit.find_next()

# Navigation

# The reason for these spoken forms is that "page up" and "page down" are globally defined as keys.
scroll up: edit.page_up()
scroll down: edit.page_down()

go word left: edit.word_left()
go word right: edit.word_right()

go left: edit.left()
go right: edit.right()
go up: edit.up()
go down: edit.down()

go line start | head: edit.line_start()
go line end | tail: edit.line_end()

go way left:
    edit.line_start()
    edit.line_start()
go way right: edit.line_end()
go way up: edit.file_start()
go way down: edit.file_end()

go top: edit.file_start()
go bottom: edit.file_end()

go page up: edit.page_up()
go page down: edit.page_down()

# Selecting
select all: edit.select_all()
select line: edit.select_line()
select line start: user.select_line_start()
select line end: user.select_line_end()
select block: edit.select_paragraph()

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

# Indentation
indent [more]: edit.indent_more()
(indent less | out dent): edit.indent_less()

# Delete
clear all: user.delete_all()
clear line: edit.delete_line()
clear line start: user.delete_line_start()
clear line end: user.delete_line_end()
clear block: edit.delete_paragraph()
clear left: edit.delete()
clear right: user.delete_right()

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

# Copy
copy that: edit.copy()
copy append that: user.copy_append()
copy all: user.copy_all()
copy line: user.copy_line()
copy line start: user.copy_line_start()
copy line end: user.copy_line_end()
copy block: user.copy_paragraph()
copy word: user.copy_word()
copy word left: user.copy_word_left()
copy word right: user.copy_word_right()

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

# Cut
cut that: edit.cut()
cut append that: user.cut_append()
cut all: user.cut_all()
cut line: user.cut_line()
cut line start: user.cut_line_start()
cut line end: user.cut_line_end()
cut block: user.cut_paragraph()
cut word: user.cut_word()
cut word left: user.cut_word_left()
cut word right: user.cut_word_right()

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

# Paste
(pace | paste) that: edit.paste()
(pace | paste) enter:
    edit.paste()
    key(enter)
paste match: edit.paste_match_style()
(pace | paste) [to] all: user.paste_all()
(pace | paste) [to] line: user.paste_line()
(pace | paste) [to] line start: user.paste_line_start()
(pace | paste) [to] line end: user.paste_line_end()
(pace | paste) [to] block: user.paste_paragraph()
(pace | paste) [to] word: user.paste_word()

# Duplication
clone that: edit.selection_clone()
clone line: edit.line_clone()

# Insert new line
new line above: edit.line_insert_up()
new line below | slap: edit.line_insert_down()

# Insert padding with optional symbols
(pad | padding): user.insert_between(" ", " ")
(pad | padding) <user.symbol_key>+:
    insert(" ")
    user.insert_many(symbol_key_list)
    insert(" ")

# Undo/redo
undo that: edit.undo()
redo that: edit.redo()

# Save
file save: edit.save()
file save all: edit.save_all()

[go] line mid: user.line_middle()
