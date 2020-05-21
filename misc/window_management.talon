os: linux
#os: windows
-

maximize window: user.window_maximize()
minimize window: user.window_minimize()

new window: app.window_open()
next window: app.window_next()
last window: app.window_previous()
close window: app.window_close()
focus <user.running_applications>: user.switcher_focus(running_applications)
list running: user.switcher_list_running()
hide running: user.switcher_hide_running()
