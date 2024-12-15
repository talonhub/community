tag: user.multiple_cursors
-
dart multiple: user.multi_cursor_enable()
dart stop: user.multi_cursor_disable()
dart up [<number_small>]:
	numb  = number_small or 1
    user.multi_cursor_add_above()
    repeat(numb - 1)
dart down [<number_small>]: 
	numb  = number_small or 1
    user.multi_cursor_add_below()
    repeat(numb - 1)
dart less [<number_small>]:
    numb  = number_small or 1
    user.multi_cursor_select_fewer_occurrences()
    repeat(numb - 1)
dart more [<number_small>]: 
	numb  = number_small or 1
    user.multi_cursor_select_more_occurrences()
    repeat(numb - 1)
dart skip: user.multi_cursor_skip_occurrence()
dart all: user.multi_cursor_select_all_occurrences()
dart lines: user.multi_cursor_add_to_line_ends()
