os: windows
-
new window: app.window_open()

switch window: user.window_last()

maximize window: user.window_maximize()
minimize window: user.window_minimize()

next window: app.window_next()
(prior | previous | last) window: app.window_previous()
select window: user.window_select()

close window: app.window_close()
focus <user.running_applications>: user.switcher_focus(running_applications)
list running: user.switcher_list_running()
hide running: user.switcher_hide_running()

move window left: user.window_move_left_screen()
move window right: user.window_move_right_screen()

snap window left: user.window_snap_left()
snap window right: user.window_snap_right()
