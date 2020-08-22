find it:
    edit.find()

next one:
    edit.find_next()

go word left:
    edit.word_left()

go word right:
    edit.word_right()

go left:
    edit.left()

go right:
    edit.right()

go up:
    edit.up()

go down:
    edit.down()

go line start:
    edit.line_start()

go line end:
    edit.line_end()

go way left:
    edit.line_start()
    edit.line_start()

go way right:
    edit.line_end()

go way down:
    edit.file_end()

go way up:
    edit.file_start()

go page down:
    edit.page_down()

go page up:
    edit.page_up()

# selecting
select line:
    edit.line_start()
    edit.extend_line_end()

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

select word left:
    edit.extend_word_left()

select word right:
    edit.extend_word_right()

select way left:
    edit.extend_line_start()

select way right:
    edit.extend_line_end()

select way up:
    edit.extend_file_start()

select way down:
    edit.extend_file_end()

# editing
indent [more]:
    edit.indent_more()

(indent less | out dent):
    edit.indent_less()

# deleting
exile line:
    edit.delete_line()

exile left:
    key(backspace)

exile right:
    key(delete)

exile up:
    edit.extend_line_up()
    edit.delete()

exile down:
    edit.extend_line_down()
    edit.delete()

exile word left:
    edit.extend_word_left()
    edit.delete()

exile word right:
    edit.extend_word_right()
    edit.delete()

exile way left:
    edit.extend_line_start()
    edit.delete()

exile way right:
    edit.extend_line_end()
    edit.delete()

exile way up:
    edit.extend_file_start()
    edit.delete()

exile way down:
    edit.extend_file_end()
    edit.delete()
