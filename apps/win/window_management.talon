os: windows
-
new window: app.window_open()

last window: user.window_last()

next window: app.window_next()
previous window: app.window_previous()
select window: user.window_select()

close window: app.window_close()
focus <user.running_applications>: user.switcher_focus(running_applications)
list running: user.switcher_list_running()
hide running: user.switcher_hide_running()
