os: windows
tag: user.thumbnail_switcher_all
-
focus: user.thumbnail_switcher_show_apps()
start: user.thumbnail_switcher_launcher_layout(1)
#focus | start (details): user.thumbnail_switcher_launcher_layout(1)
#start: user.thumbnail_switcher_launcher_layout(0)
layout {user.thumbnail_switcher_layouts}: user.thumbnail_switcher_place(thumbnail_switcher_layouts)
focus <user.running_applications>: 
    user.switcher_focus(running_applications)
start <user.launch_applications>: user.switcher_launch(launch_applications)