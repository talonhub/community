tag: line_commands
-
<user.selection_verbs> word: user.select_word(selection_verbs)
<user.selection_verbs> whole line <number>: user.select_whole_line(selection_verbs, number)
<user.selection_verbs> [line] <number>: user.select_line(selection_verbs, number)

#note: the below command generally requires some sort of RPC
<user.selection_verbs> until <number>: user.select_until_line(selection_verbs, number)

<user.selection_verbs> <number> until <number>: user.select_range(selection_verbs, number_1, number_2)
<user.selection_verbs> this: user.select_current_line(selection_verbs)
<user.selection_verbs> way left: user.select_way_left(selection_verbs)
<user.selection_verbs> way right: user.select_way_right(selection_verbs)
<user.selection_verbs> way up: user.select_way_up(selection_verbs)
<user.selection_verbs> way down: user.select_way_down(selection_verbs)

#note: camel selection may not be supported by all applications.
<user.selection_verbs> camel left: user.select_camel_left(selection_verbs)
<user.selection_verbs> camel right: user.select_camel_right(selection_verbs)

<user.selection_verbs> all: user.select_all(selection_verbs)
<user.selection_verbs> left: user.select_left(selection_verbs)
<user.selection_verbs> right: user.select_right(selection_verbs)
<user.selection_verbs> up: user.select_up(selection_verbs)
<user.selection_verbs> down: user.select_down(selection_verbs)
<user.selection_verbs> word left: user.select_word_left(selection_verbs)
<user.selection_verbs> word right: user.select_word_right(selection_verbs)

# Select verb/object
<user.selection_verbs> next <user.text> [over]: user.select_next_occurrence(selection_verbs, text)
<user.selection_verbs> last <user.text> [over]: user.select_previous_occurrence(selection_verbs, text)

<user.selection_verbs> next clippy: user.select_next_occurrence(selection_verbs, clip.text())
<user.selection_verbs> last clippy: user.select_previous_occurrence(selection_verbs, clip.text())

# Movement
<user.navigation_verbs> [line] <number>: user.go_to_line(navigation_verbs, number)
<user.navigation_verbs> [line] <number> end: user.go_to_line_end(navigation_verbs, number)

<user.navigation_verbs> next <user.text> [over]: user.move_next_occurrence(navigation_verbs, text)
<user.navigation_verbs> last <user.text> [over]: user.move_previous_occurrence(navigation_verbs, text)

<user.navigation_verbs> next clippy: user.move_next_occurrence(navigation_verbs, clip.text())
<user.navigation_verbs> last clippy: user.move_previous_occurrence(navigation_verbs, clip.text())

#camel movement, may not be supported by all applications that opt-in.
<user.navigation_verbs> camel left: user.move_camel_left(navigation_verbs)
<user.navigation_verbs> camel right: user.move_camel_right(navigation_verbs)

lend: edit.line_end()
bend: edit.line_start()
drag [line] up: edit.line_swap_up()
drag [line] down: edit.line_swap_down()
clone (line|this): edit.line_clone()

#may not be supportable without some sort of RPC?
clone [line] <number>: user.line_clone(number)


