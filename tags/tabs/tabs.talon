tag: user.tabs
-

# Creation
tab (open | new): app.tab_open()
tab (open | new) named [<user.text>]: user.tab_open_with_name(text or "")
tab (reopen | restore): app.tab_reopen()
tab (clone | duplicate): user.tab_clone()

# Destruction
tab close: user.tab_close_wrapper()
tab close all: user.tab_close_all()
tab (close others | solo): user.tab_close_others()

# Navigation
[go] tab (last | previous): app.tab_previous()
[go] tab next: app.tab_next()
[go] tab <number>: user.tab_focus_index(number)
[go] tab minus <number>: user.tab_focus_negative_index(number)
[go] tab first: user.tab_focus_first()
[go] tab final: user.tab_focus_final()
[go] tab flip: user.tab_focus_most_recent()
[go] tab named <user.text>: user.tab_focus_named(text)
tab search [<user.text>]: user.tab_search(text or "")

# Arrangement
tab pin: user.tab_pin()
tab unpin: user.tab_unpin()
tab move right: user.tab_move_right()
tab move left: user.tab_move_left()
tab move to split right: user.tab_move_to_split_right()
tab move to split left: user.tab_move_to_split_left()
tab move [to split] up: user.tab_move_to_split_up()
tab move [to split] down: user.tab_move_to_split_down()

# Renaming
tab rename [<user.text>]: user.tab_rename_formatted(text or "")
tab [name] reset: user.tab_reset_name()
