# see app/vscode_generic.talon for linux and windows action implementation 

app: /Code.*/
-

# editing
code refactor all: user.ide_refactor()
code refactor: user.ide_refactor_in_line()
code rename: user.ide_refactor_rename()
code follow: user.ide_follow()
code comment: user.ide_toggle_comment()
code suggest: user.ide_smart()
code arguments: user.ide_parameter_hints()
code done: user.ide_done()

# navigating
go back: user.ide_go_back()
go forward: user.ide_go_forward()

# selection
cursor up: user.ide_up_cursor()
cursor down: user.ide_down_cursor()

# debugging
step over: user.ide_step_over()
step into: user.ide_step_into()
step continue: user.ide_continue()

# terminal
console: user.ide_toggle_terminal()
console new: user.ide_terminal_new()
console next: user.ide_terminal_focus_next()
console trash: user.ide_terminal_trash()
console last: user.ide_terminal_focus_previous()
console up: user.ide_terminal_scroll_up()
console down: user.ide_terminal_scroll_down()

# focus
show explorer: user.ide_show_explorer()
show search: user.ide_show_search()
show source control: user.ide_show_source_control()
show debug: user.ide_show_debug()
show extensions: user.ide_show_extensions()