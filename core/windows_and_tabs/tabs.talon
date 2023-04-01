tag: user.tabs
-
tab (open | new): app.tab_open()
tab (last | previous): app.tab_previous()
tab next: app.tab_next()
tab close: user.tab_close_wrapper()
tab close <number_small>: 
    user.tab_close_wrapper()
    repeat(number_small-1)
tab (reopen | restore): app.tab_reopen()
go tab <number>: user.tab_jump(number)
go tab final: user.tab_final()
tab duplicate: user.tab_duplicate()
tab close others: user.tab_close_others()
tab close all: user.tab_close_all()
tab close right: user.tab_close_right()
tab close left: user.tab_close_left()
tab search: user.tab_search("")
^tab search <user.text>$: user.tab_search(text or "")