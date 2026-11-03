tag: user.thumbnail_switcher_showing
-
<number_small>: user.thumbnail_switcher_select(number_small)
pick <number_small>: user.thumbnail_switcher_select(number_small)
thumbs close: user.thumbnail_switcher_hide()
thumbs search <user.text>: user.thumbnail_switcher_search(text)
thumbs app <user.running_applications>: user.thumbnail_switcher_app(running_applications)
thumbs clear: user.thumbnail_switcher_clear()

# Managing windows by their number in the switcher. Numbers can be combined, e.g.
# "close two and five" or "snap one and three half".
(close | win close) <user.thumbnail_switcher_numbers>:
    user.thumbnail_switcher_close(thumbnail_switcher_numbers)
(min | minimize) <user.thumbnail_switcher_numbers>:
    user.thumbnail_switcher_minimize(thumbnail_switcher_numbers)
(restore | unmin) <user.thumbnail_switcher_numbers>:
    user.thumbnail_switcher_restore(thumbnail_switcher_numbers)
(max | maximize) <number_small>: user.thumbnail_switcher_maximize(number_small)
snap <number_small> <user.window_snap_position>:
    user.thumbnail_switcher_snap(number_small, window_snap_position)
snap <number_small> screen <number_small>:
    user.thumbnail_switcher_move_to_screen(number_small_1, number_small_2)
snap <number_small> next screen: user.thumbnail_switcher_move_next_screen(number_small)
snap <number_small> last screen: user.thumbnail_switcher_move_previous_screen(number_small)
snap <user.thumbnail_switcher_numbers> {user.thumbnail_switcher_layouts}:
    user.thumbnail_switcher_layout(thumbnail_switcher_numbers, thumbnail_switcher_layouts)

# Virtual desktops: move windows by number, or filter to one desktop.
desk <user.thumbnail_switcher_numbers> to <number_small>:
    user.thumbnail_switcher_move_to_desktop(thumbnail_switcher_numbers, number_small)
desk <user.thumbnail_switcher_numbers> next:
    user.thumbnail_switcher_move_next_desktop(thumbnail_switcher_numbers)
desk <user.thumbnail_switcher_numbers> last:
    user.thumbnail_switcher_move_previous_desktop(thumbnail_switcher_numbers)
thumbs desk <number_small>: user.thumbnail_switcher_desk(number_small)

# Fill a layout slot by slot: say a window's number for each slot in turn.
layout {user.thumbnail_switcher_layouts}: user.thumbnail_switcher_place(thumbnail_switcher_layouts)
skip: user.thumbnail_switcher_skip()
cancel: user.thumbnail_switcher_cancel()
menu <number_small>: user.thumbnail_switcher_menu(number_small)
# In the apps view: the windows of one app.
windows <number_small>: user.thumbnail_switcher_app_windows(number_small)
thumbs screen <number_small>: user.thumbnail_switcher_screen(number_small)

# Marking several windows, then acting on all of them. Marks survive the search;
# saying a number (or "pick") still focuses one window.
mark <user.thumbnail_switcher_numbers>:
    user.thumbnail_switcher_mark(thumbnail_switcher_numbers)
mark <number_small> (through | until) <number_small>:
    user.thumbnail_switcher_mark_range(number_small_1, number_small_2)
unmark <user.thumbnail_switcher_numbers>:
    user.thumbnail_switcher_unmark(thumbnail_switcher_numbers)
mark all: user.thumbnail_switcher_mark_all()
(unmark all | mark clear): user.thumbnail_switcher_clear_marks()
menu marked: user.thumbnail_switcher_marked_menu()
(close | win close) marked: user.thumbnail_switcher_close_marked()
(min | minimize) marked: user.thumbnail_switcher_minimize_marked()
(restore | unmin) marked: user.thumbnail_switcher_restore_marked()
snap marked {user.thumbnail_switcher_layouts}:
    user.thumbnail_switcher_layout_marked(thumbnail_switcher_layouts)
snap marked screen <number_small>: user.thumbnail_switcher_move_marked_to_screen(number_small)
snap marked next screen: user.thumbnail_switcher_move_marked_next_screen()
snap marked last screen: user.thumbnail_switcher_move_marked_previous_screen()
desk marked to <number_small>: user.thumbnail_switcher_move_marked_to_desktop(number_small)
desk marked next: user.thumbnail_switcher_move_marked_next_desktop()
desk marked last: user.thumbnail_switcher_move_marked_previous_desktop()

# In the app launcher (and the apps strip): another instance of an app.
launch new <number_small>: user.thumbnail_switcher_launch_new(number_small)
# In the app launcher: jump to the apps starting with a letter.
jump <user.letter>: user.thumbnail_switcher_jump(letter)
jump (number | numbers | symbol): user.thumbnail_switcher_jump("#")
# In the app launcher's details view.
sort by {user.thumbnail_switcher_columns}: user.thumbnail_switcher_sort(thumbnail_switcher_columns)
sort default: user.thumbnail_switcher_sort("")
