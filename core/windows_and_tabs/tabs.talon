tag: user.tabs
-
tab (open | new): app.tab_open()
tab (reopen | restore): app.tab_reopen()
tab (duplicate | clone): user.tab_duplicate()
tab close: user.tab_close_wrapper()

tab (last | previous): app.tab_previous()
tab next: app.tab_next()
go tab <number>: user.tab_jump(number)
go tab final: user.tab_final()
