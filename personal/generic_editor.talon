copy line:
    edit.line_start()
    edit.extend_line_end()
    edit.copy()

cut line:
    edit.line_start()
    edit.extend_line_end()
    edit.cut()

boom line:
    edit.delete_line()
    key(shift-up shift-end)
    edit.delete()

go less right:
    edit.line_end()
    edit.left()

clear this:
    edit.word_right()
    edit.extend_word_left()
    edit.delete()

fate <user.text>:
    key(ctrl-f)
    insert(user.text)
    key(enter)

go south:
    edit.down()
    edit.line_start()

go north:
    edit.up()
    edit.line_end()