tag: user.splits
-

# Creation

## Empty splits
split [create] right: user.split_create_right()
split [create] left: user.split_create_left()
split [create] down: user.split_create_down()
split [create] up: user.split_create_up()
split [create] (vertically | vertical): user.split_create_vertically()
split [create] (horizontally | horizontal): user.split_create_horizontally()
split (new|create): user.split_create()

## Duplicated splits
split clone right: user.split_clone_right()
split clone left: user.split_clone_left()
split clone down: user.split_clone_down()
split clone up: user.split_clone_up()
split clone (vertically | vertical): user.split_clone_vertically()
split clone (horizontally | horizontal): user.split_clone_horizontally()
split clone (new|create): user.split_clone()

# Destruction
split close: user.split_close()
split close all: user.split_close_all()

# Navigation
cross right: user.split_focus_right()
cross left: user.split_focus_left()
cross down: user.split_focus_down()
cross up: user.split_focus_up()
cross next: user.split_focus_next()
cross (last|previous): user.split_focus_previous()
cross first: user.split_focus_first()
cross final: user.split_focus_final()
cross flip: user.split_focus_most_recent()
(go split|cross) <number>: user.split_focus_index(number)
(go split|cross) minus <number>: user.split_focus_negative_index(number)

# Arrangement
split move right: user.split_move_right()
split move left: user.split_move_left()
split move down: user.split_move_down()
split move up: user.split_move_up()
split move next tab: user.split_move_next_tab()
split move (last|previous) tab: user.split_move_previous_tab()
split move new tab: user.split_move_new_tab()
split toggle zen: user.split_toggles_zen()
split rotate right: user.split_rotate_right()
split rotate left: user.split_rotate_left()
split axis: user.split_toggle_orientation()

# Resizing
split max: user.split_toggle_maximize()
split reset: user.split_layout_reset()
split expand: user.split_expand()
split (wider|expand width): user.split_expand_width()
split (taller|expand height): user.split_expand_height()
split shrink: user.split_shrink()
split (thinner|shrink width): user.split_shrink_width()
split (shorter|shrink height): user.split_shrink_height()
split set width <number>: user.split_set_width(number)
split set height <number>: user.split_set_height(number)

# Deprecated
split window: user.split_window()
split clear: user.split_clear()
split clear all: user.split_clear_all()
split center: user.split_center()
split flip: user.split_flip()
