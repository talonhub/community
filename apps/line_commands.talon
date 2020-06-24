tag: line_commands
-
#<user.select_verbs> this: user.idea_select(select_verbs)
<user.select_verbs> whole line <number>: user.select_line(select_verbs, number)
<user.select_verbs> line <number>: user.select_line(select_verbs, number)
<user.select_verbs> until line <number>: user.select_until_line(select_verbs, number)
<user.select_verbs> <number> until <number>: user.select_range(select_verbs, number_1, number_2)
<user.select_verbs> line: user.select_current_line(select_verbs)
<user.select_verbs> way left: user.select_way_left(select_verbs)
<user.select_verbs> way right: user.select_way_right(select_verbs)
<user.select_verbs> way up: user.select_way_up(select_verbs)
<user.select_verbs> way down: user.select_way_down(select_verbs)
<user.select_verbs> camel left: user.select_camel_left(select_verbs)
<user.select_verbs> camel right: user.select_camel_right(select_verbs)

<user.select_verbs> all: user.select_all(select_verbs)
<user.select_verbs> left: user.select_left(select_verbs)
<user.select_verbs> right: user.select_right(select_verbs)
<user.select_verbs> up: user.select_up(select_verbs)
<user.select_verbs> down: user.select_down(select_verbs)
<user.select_verbs> word left: user.select_word_left(select_verbs)
<user.select_verbs> word right: user.select_word_right(select_verbs)

#<user.select_verbs> next <phrase> [over]: user.idea_select(select_verbs, "find next {phrase}")
#<user.select_verbs> last <phrase> [over]: user.idea_select(select_verbs, "find prev {phrase}")

# Movement
go line <number>: user.go_to_line(number)

#todo
#<user.movement_verbs> next (error | air): 
#<user.movement_verbs> last (error | air): 
<user.movement_verbs> camel left: user.move_camel_left(movement_verbs)
<user.movement_verbs> camel right: user.move_camel_right(movement_verbs)

#<user.movement_verbs> next <phrase> [over]: user.idea_movement(movement_verbs, "find next {phrase}, action EditorRight")
#<user.movement_verbs> last <phrase> [over]: user.idea_movement(movement_verbs, "find prev {phrase}, action EditorRight")