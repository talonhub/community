tag: user.tabs
-
tab (open | new): app.tab_open()
tab previous: app.tab_previous()
tab next: app.tab_next()
tab close: user.tab_close_wrapper()
tab (reopen | restore): app.tab_reopen()
tab num <number>: user.tab_jump(number)
tab last: user.tab_final()
tab first: user.tab_jump(1)
tab (duplicate | clone): user.tab_duplicate()