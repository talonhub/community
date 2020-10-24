window (new|open): app.window_open()
window next: app.window_next()
window last: app.window_previous()
window close: app.window_close()
focus <user.running_applications>: user.switcher_focus(running_applications)
<<<<<<< HEAD
running list: user.switcher_toggle_running()
launch <user.launch_applications>: user.switcher_launch(launch_applications)

snap <user.window_snap_position>: user.snap_window(window_snap_position)
snap next [screen]: user.move_window_next_screen()
snap last [screen]: user.move_window_previous_screen()
snap screen <number>: user.move_window_to_screen(number)
snap <user.running_applications> <user.window_snap_position>:
    user.snap_app(running_applications, window_snap_position)
snap <user.running_applications> [screen] <number>:
    user.move_app_to_screen(running_applications, number)
=======
list running: user.switcher_list_running()
hide running: user.switcher_hide_running()

put window left: key(ctrl-alt-left)
put window right: key(ctrl-alt-right)
put window up: key(ctrl-alt-up)
put window next: key(ctrl-shift-alt-up)

put window way left: key(ctrl-cmd-alt-left)
put window way right: key(ctrl-cmd-alt-right)

>>>>>>> master
