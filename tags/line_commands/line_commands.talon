tag: user.line_commands
-
#this defines some common row commands. More may be defined that are ide-specific.
# lend: edit.line_end()
# bend: edit.line_start()
row <number>: edit.jump_line(number)
row <number> end: 
    edit.jump_line(number)
    edit.line_end()
note [row] <number>:
    user.select_range(number, number)
    code.toggle_comment()
note <number> by <number>: 
    user.select_range(number_1, number_2)
    code.toggle_comment()
(mop | wipe row) <number>:
    edit.jump_line(number)
    user.select_range(number, number)
    edit.delete()
(mop | wipe row) <number> by <number>: 
    user.select_range(number_1, number_2)
    edit.delete()
copy [row] <number>: 
    user.select_range(number, number)
    edit.copy()
copy <number> by <number>: 
    user.select_range(number_1, number_2)
    edit.copy()
snip [row] <number>: 
    user.select_range(number, number)
    edit.cut()
snip [row] <number> by <number>: 
    user.select_range(number_1, number_2)
    edit.cut()
paste <number> by <number>:
  user.select_range(number_1, number_2)
  edit.paste()
replace <number> by <number>: 
    user.select_range(number_1, number_2)
    edit.paste()
grab [row] <number>: user.select_range(number, number)
(grab [row] | row) <number> by <number>: user.select_range(number_1, number_2)
tab [row] <number>:
    edit.jump_line(number)
    edit.indent_more() 
tab <number> by <number>:
    user.select_range(number_1, number_2)
    edit.indent_more()
# retab that: edit.indent_less()
retab [row] <number>:
    user.select_range(number, number)
    edit.indent_less()
retab <number> by <number>:
    user.select_range(number_1, number_2)
    edit.indent_less()
drag [row] down: edit.line_swap_down()
drag [row] up: edit.line_swap_up()
drag up [row] <number>:
    user.select_range(number, number)
    edit.line_swap_up()
drag up <number> by <number>: 
    user.select_range(number_1, number_2)
    edit.line_swap_up()
drag down [row] <number>: 
    user.select_range(number, number)
    edit.line_swap_down()
drag down <number> by <number>: 
    user.select_range(number_1, number_2)
    edit.line_swap_down()
clone row: edit.line_clone()
