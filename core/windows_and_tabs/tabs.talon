tag: user.tabs
-
tab (open | new) [<number_small>]: 
    number = number_small  or 1
    app.tab_open()
    repeat(number - 1)
tab (last | previous): app.tab_previous()
tab next: app.tab_next()
tab (close|clothes|cloth|kill): user.tab_close_wrapper()
tab (close|clothes|cloth|kill) <number_small>: 
    user.tab_close_wrapper()
    repeat(number_small-1)
tab (reopen | restore): app.tab_reopen()
go tab <number>: user.tab_jump(number)
go tab final: user.tab_final()
tab duplicate: user.tab_duplicate()
tab (close|clothes|cloth|kill) others: user.tab_close_others()
tab (close|clothes|cloth|kill) other: user.tab_close_others()
tab (close|clothes|cloth|kill) all: user.tab_close_all()
tab (close|clothes|cloth|kill) right: user.tab_close_right()
tab (close|clothes|cloth|kill) left: user.tab_close_left()
tab search: user.tab_search("")
^tab search <user.text>$: user.tab_search(text or "")