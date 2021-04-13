tag: user.line_commands
-
#this defines some common line commands. More may be defined that are ide-specific.
paste line:
    edit.line_end()
	key(enter)
    edit.paste()
paste line up:
    edit.line_start()
    key(left)
	key(enter)
    edit.paste()
# go <number> start: edit.jump_line(number)
# go <number> end: 
#     edit.jump_line(number)
#     edit.line_end()
comment (line | this | that):
    code.toggle_comment()
add comment <user.text>$:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    code.toggle_comment()
    insert(user.text)
# comment <number> until <number>: 
#     user.select_range(number_1, number_2)
#     code.toggle_comment()
# <user.delete> line <number>:
#     edit.jump_line(number)
#     user.select_range(number, number)
#     edit.delete()
# <user.delete> <number> until <number>: 
#     user.select_range(number_1, number_2)
#     edit.delete()
# copy [line] <number>: 
#     user.select_range(number, number)
#     edit.copy()
# copy <number> until <number>: 
#     user.select_range(number_1, number_2)
#     edit.copy()
# cut line <number>: 
#     user.select_range(number, number)
#     edit.cut()
# cut line <number> until <number>: 
#     user.select_range(number_1, number_2)
#     edit.cut()
# (paste | replace) <number> until <number>:
#     user.select_range(number_1, number_2)
#     edit.paste()
# (select | cell | sell) [line] <number>: user.select_range(number, number)
# (select | cell | sell) <number> until <number>: user.select_range(number_1, number_2)
tab that: edit.indent_more()
# tab line <number>:
#     edit.jump_line(number)
#     edit.indent_more()
# tab <number> until <number>:
#     user.select_range(number_1, number_2)
#     edit.indent_more()
# retab that: edit.indent_less()
# retab [line] <number>:
#     user.select_range(number, number)
#     edit.indent_less()
# retab <number> until <number>:
#     user.select_range(number_1, number_2)
#     edit.indent_less()
drag line down: edit.line_swap_down()
drag line up: edit.line_swap_up()
# drag up [line] <number>:
#     user.select_range(number, number)
#     edit.line_swap_up()
# drag up <number> until <number>: 
#     user.select_range(number_1, number_2)
#     edit.line_swap_up()
# drag down [line] <number>: 
#     user.select_range(number, number)
#     edit.line_swap_down()
# drag down <number> until <number>: 
#     user.select_range(number_1, number_2)
#     edit.line_swap_down()
smear (line|that): edit.line_clone()
