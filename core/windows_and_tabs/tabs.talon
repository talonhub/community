tag: user.tabs
-
tab (open | new): app.tab_open()
tab (last | previous): app.tab_previous()
tab next: app.tab_next()
tab (reopen | restore): app.tab_reopen()

tab close: user.tab_close_wrapper()
go tab <number>: user.tab_jump(number)
go tab final: user.tab_final()
tab duplicate: user.tab_duplicate()
tab search: user.tab_search()
tab pin: user.tab_pin()
tab unpin: user.tab_unpin()
tab rename [<user.text>]: user.tab_rename_wrapper(text or "")
tab flip: user.tab_focus_most_recent()
tab move left: user.tab_move_left()
tab move right: user.tab_move_right()
