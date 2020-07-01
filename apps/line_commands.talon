tag: line_commands
-
#<user.selection_verbs> this line: user.idea_select(selection_verbs)
<user.selection_verbs> whole line <number>: user.select_whole_line(selection_verbs, number)
<user.selection_verbs> line <number>: user.select_line(selection_verbs, number)
#<user.selection_verbs> until line <number>: user.select_until_line(selection_verbs, number)
<user.selection_verbs> <number> until <number>: user.select_range(selection_verbs, number_1, number_2)
<user.selection_verbs> line: user.select_current_line(selection_verbs)
<user.selection_verbs> way left: user.select_way_left(selection_verbs)
<user.selection_verbs> way right: user.select_way_right(selection_verbs)
<user.selection_verbs> way up: user.select_way_up(selection_verbs)
<user.selection_verbs> way down: user.select_way_down(selection_verbs)
<user.selection_verbs> camel left: user.select_camel_left(selection_verbs)
<user.selection_verbs> camel right: user.select_camel_right(selection_verbs)

<user.selection_verbs> all: user.select_all(selection_verbs)
<user.selection_verbs> left: user.select_left(selection_verbs)
<user.selection_verbs> right: user.select_right(selection_verbs)
<user.selection_verbs> up: user.select_up(selection_verbs)
<user.selection_verbs> down: user.select_down(selection_verbs)
<user.selection_verbs> word left: user.select_word_left(selection_verbs)
<user.selection_verbs> word right: user.select_word_right(selection_verbs)

# Movement
<user.navigation_verbs> line <number>: user.go_to_line(number, navigation_verbs)
#<user.navigation_verbs> next (error | air): user.ide_next_error(navigation_verbs)
#<user.navigation_verbs> last (error | air): user.ide_last_error(navigation_verbs)
#<user.navigation_verbs> camel left: user.move_camel_left(navigation_verbs)
#<user.navigation_verbs> camel right: user.move_camel_right(navigation_verbs)
