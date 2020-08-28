tag: user.line_commands
-
#this defines some common commands. More may be defined that are ide-specific.
lend: edit.line_end()
bend: edit.line_start()
go <number>: edit.jump_line(number)
go <number> end: 
    edit.jump_line(number)
    edit.line_end()
comment line <number>:
    user.select_range(number, number)
    code.toggle_comment()
comment <number> until <number>: 
    user.select_range(number_1, number_2)
    code.toggle_comment()
clear line <number>:
    edit.jump_line(number)
    user.select_range(number, number)
    edit.delete()
clear <number> until <number>: 
    user.select_range(number_1, number_2)
    edit.delete()
copy line <number>: 
    user.select_range(number, number)
copy <number> until <number>: 
    user.select_range(number_1, number_2)
    edit.copy()
cut line <number>: 
    user.select_range(number, number)
    edit.cut()
cut <number> until <number>: 
    user.select_range(number_1, number_2)
    edit.cut()
paste <number> until <number>:
  user.select_range(number_1, number_2)
  edit.paste()
replace <number> until <number>: 
    user.select_range(number_1, number_2)
    edit.paste()
select line <number>: user.select_range(number, number)
select <number> until <number>: user.select_range(number_1, number_2)
indent <number>:
    edit.jump_line(number)
    edit.indent_more()
indent <number> until <number>:
    user.select_range(number_1, number_2)
    edit.indent_more()
unindent line <number>:
    user.select_range(number, number)
    edit.indent_less()
unindent <number> until <number>:
    user.select_range(number_1, number_2)
    edit.indent_less()
drag [line] down: edit.line_swap_down()
drag [line] up: edit.line_swap_up()
drag up <number>:
    user.select_range(number, number)
    edit.line_swap_up()
drag up <number> until <number>: 
    user.select_range(number_1, number_2)
    edit.line_swap_up()
drag down <number>: 
    user.select_range(number, number)
    edit.line_swap_down()
drag down <number> until <number>: 
    user.select_range(number_1, number_2)
    edit.line_swap_down()
clone (line|this): edit.line_clone()
