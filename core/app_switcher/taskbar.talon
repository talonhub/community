os: windows
os: mac
-
# [focus] {user.running_applications}:
#     user.switcher_accessibility_focus(running_applications)
<number_small>: 
    user.taskbar_click(0, number_small - 1)

<number_small> connie: 
    user.taskbar_click(1, number_small - 1)

tray hidden:
    user.system_tray_show_hidden()

tray <number_small>:
    user.system_tray_click(0, number_small - 1)

tray <number_small> connie:
    user.system_tray_click(1, number_small - 1)
