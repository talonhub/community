window (new|open): app.window_open()
window next: app.window_next()
window last: app.window_previous()
window close: app.window_close()
focus <user.running_applications>: user.switcher_focus(running_applications)
running list: user.switcher_toggle_running()
launch <user.launch_applications>: user.switcher_launch(launch_applications)

snap <user.window_snap_position>: user.snap_window(window_snap_position)
snap full|sol for|snap for:
    user.snap_window_full()
snap next full:
    user.move_window_next_screen()
    user.snap_window_full()
snap last full:
    user.move_window_previous_screen()
    user.snap_window_full()

# fido: user.snap_window() 
(snap|star|nap|slap) next [screen]: user.move_window_next_screen()
(snap|star|nap|slap) last [screen]: user.move_window_previous_screen()
(snap|star|nap|slap) one: user.move_window_to_screen(1)
(snap|star|nap|slap) best: user.move_window_to_screen(2)
(snap|star|nap|slap) cup: user.move_window_to_screen(3)
# snap screen <number>: user.move_window_to_screen(number)
snap <user.running_applications> <user.window_snap_position>:
    user.snap_app(running_applications, window_snap_position)
snap <user.running_applications> [screen] <number>:
    user.move_app_to_screen(running_applications, number)

