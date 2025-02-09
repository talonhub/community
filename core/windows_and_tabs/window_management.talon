win (new | open): app.window_open()
win next: app.window_next()
win last: app.window_previous()
win close: app.window_close()
focus <user.running_applications>: user.switcher_focus(running_applications)
# following only works on windows. Can't figure out how to make it work for mac. No idea what the equivalent for linux would be.
focus$: user.switcher_menu()
focus last: user.switcher_focus_last()
#running list: user.switcher_toggle_running()
#running close: user.switcher_hide_running()
start <user.launch_applications>: user.switcher_launch(launch_applications)

(snap) <user.window_snap_position>: user.snap_window(window_snap_position)
snapfur: user.snap_window_to_position("full")
aprate: user.snap_window_to_position("right")
snap rat: user.snap_window_to_position("right")
<user.window_layout>: user.snap_layout(window_layout)

desk show: user.switcher_show_desktop()
