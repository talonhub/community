tag: user.tabs
-
tab (open | new): app.tab_open()
tab (reopen | restore): app.tab_reopen()
tab (duplicate | clone): user.tab_duplicate()
tab close: user.tab_close_wrapper()

tab (last | previous | left | up): app.tab_previous()
tab (next | right | down): app.tab_next()
go tab <number>: user.tab_jump(number)
go tab final: user.tab_final()

tab move (left | up): user.tab_move_left()
tab move (right | down): user.tab_move_right()
tab detach: app.tab_detach()
