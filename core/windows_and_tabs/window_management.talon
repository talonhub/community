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
snap next [screen]: user.move_window_next_screen()
snap last [screen]: user.move_window_previous_screen()
snap screen <number>: user.move_window_to_screen(number)
snap <user.running_applications> <user.window_snap_position>:
    user.snap_app(running_applications, window_snap_position)
snap split <user.running_applications> <user.running_applications>:
    user.snap_split_two(running_applications_1, running_applications_2)
snap split <user.running_applications> <user.running_applications> <user.running_applications>:
    user.snap_split_three(running_applications_1, running_applications_2, running_applications_3)
snap clock <user.running_applications> <user.running_applications> <user.running_applications>:
    user.snap_clock_three(running_applications_1, running_applications_2, running_applications_3)
snap counterclock <user.running_applications> <user.running_applications> <user.running_applications>:
    user.snap_counterclock_three(running_applications_1, running_applications_2, running_applications_3)
snap <user.running_applications> [screen] <number>:
    user.move_app_to_screen(running_applications, number)
