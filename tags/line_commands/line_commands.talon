tag: user.line_commands
-
<user.line_action> row <number> [by <number>]: 
    user.lines_command(number_1, number_2 or number_1, line_action)
row <number>: edit.jump_line(number)
clone row: edit.line_clone()

go char <user.unmodified_key>: user.jump_cursor_to_next_char(unmodified_key)
go last char <user.unmodified_key>: user.jump_cursor_to_prev_char(unmodified_key)

                            