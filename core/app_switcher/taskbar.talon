os: windows
os: mac
-
task <number_small>: 
    user.taskbar_click(0, number_small - 1)

task <number_small> cycle: 
    user.taskbar_control_click(0, number_small - 1)

task <number_small> connie: 
    user.taskbar_click(1, number_small - 1)

tray hidden:
    user.system_tray_show_hidden()

tray <number_small>:
    user.system_tray_click(0, number_small - 1)

tray <number_small> connie:
    user.system_tray_click(1, number_small - 1)

task refresh:
    user.taskbar_force_refresh()
