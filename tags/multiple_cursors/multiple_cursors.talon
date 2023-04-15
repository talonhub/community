tag: user.multiple_cursors
-
dart multiple: user.multi_cursor_enable()
dart stop: user.multi_cursor_disable()
dart up [<number_small>]:
    numb = number_small - 1
    user.multi_cursor_add_above()
    repeat(numb)
dart down: 
    numb = number_small - 1
    user.multi_cursor_add_below()
    repeat(numb)
dart less [<number_small>]:
    numb = number_small - 1
    user.multi_cursor_select_fewer_occurrences()
    repeat(numb)
dart more [<number_small>]: 
    numb = number_small - 1
    user.multi_cursor_select_more_occurrences()
    repeat(numb)
dart skip: user.multi_cursor_skip_occurrence()
dart all: user.multi_cursor_select_all_occurrences()
dart lines: user.multi_cursor_add_to_line_ends()
