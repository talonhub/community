tag: user.tabs
-

tab (open | new): app.tab_open()
tab <user.spatial_previous_next>: user.tab_go(spatial_previous_next)
tab close: user.tab_close_wrapper()
tab (reopen | restore): app.tab_reopen()
go tab <number>: user.tab_jump(number)
go tab final: user.tab_final()
tab (duplicate | clone): user.tab_duplicate()
