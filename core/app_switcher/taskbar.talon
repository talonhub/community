os: windows
os: mac
-
# [focus] {user.running_applications}:
#     user.switcher_accessibility_focus(running_applications)
task <number_small>: 
    user.switcher_click(0, number_small - 1)

task <number_small> connie: 
    user.switcher_click(1, number_small - 1)
