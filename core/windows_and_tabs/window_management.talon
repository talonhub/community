win (new | open): app.window_open()
win next: app.window_next()
win last: app.window_previous()
win close: app.window_close()
focus <user.running_applications>: user.switcher_focus(running_applications)
# following only works on windows. Can't figure out how to make it work for mac. No idea what the equivalent for linux would be.
focus$: user.switcher_menu()
#running list: user.switcher_toggle_running()
#running close: user.switcher_hide_running()
start <user.launch_applications>: user.switcher_launch(launch_applications)

(tick) <user.window_snap_position>: user.snap_window(window_snap_position)
(tick) next [screen]: user.move_window_next_screen()
(tick) last [screen]: user.move_window_previous_screen()
(tick) screen <number>: user.move_window_to_screen(number)
(tick) <user.running_applications> <user.window_snap_position>:
    user.snap_app(running_applications, window_snap_position)
(tick) <user.running_applications> [screen] <number>:
    user.move_app_to_screen(running_applications, number)
desk show: user.switcher_show_desktop()
