window (new | open): app.window_open()
window next: app.window_next()
window last: app.window_previous()
window close: app.window_close()
window hide: app.window_hide()
focus <user.running_applications>: user.switcher_focus(running_applications)
# following only works on windows. Can't figure out how to make it work for mac. No idea what the equivalent for linux would be.
focus$: user.switcher_menu()
focus last: user.switcher_focus_last()
running list: user.switcher_toggle_running()
running close: user.switcher_hide_running()
launch <user.launch_applications>: user.switcher_launch(launch_applications)

snap <user.window_snap_position>: user.snap_window(window_snap_position)
snap <user.ordinals_small> <user.window_snap_position>:
    user.snap_nth_window(ordinals_small, window_snap_position)
snap <user.window_pair_position> <user.running_applications>:
    user.switcher_focus(running_applications)
    user.snap_window_layout_with_focus(window_pair_position, 2, 1)
snap <user.window_trio_position> <user.running_applications>:
    user.switcher_focus(running_applications)
    user.snap_window_layout_with_focus(window_trio_position, 3, 1)
snap next [screen]: user.move_window_next_screen()
snap last [screen]: user.move_window_previous_screen()
snap screen <number>: user.move_window_to_screen(number)
snap <user.running_applications> <user.window_snap_position>:
    user.snap_app(running_applications, window_snap_position)
# <user.running_applications> is here twice to require at least two applications.
snap <user.window_pair_position> <user.running_applications> <user.running_applications>:
    user.snap_app_layout(window_pair_position, running_applications_list)
snap <user.window_trio_position> <user.running_applications> <user.running_applications> <user.running_applications>:
    user.snap_app_layout(window_trio_position, running_applications_list)
snap <user.ordinals_small> into <user.window_trio_position>:
    user.snap_window_layout_with_focus(window_trio_position, 3, ordinals_small)
snap <user.ordinals_small> into <user.window_pair_position>:
    user.snap_window_layout_with_focus(window_pair_position, 2, ordinals_small)
snap <user.window_trio_position>: user.snap_window_layout(window_trio_position, 3)
snap <user.window_pair_position>: user.snap_window_layout(window_pair_position, 2)
snap <user.running_applications> [screen] <number>:
    user.move_app_to_screen(running_applications, number)
