system shutdown:    user.system_shutdown()
system restart:     user.system_restart()
system rest:        user.system_hibernate()
system lock:        user.system_lock()
task manager:       user.system_task_manager()
desktop show:       user.system_show_desktop()
task view:          user.system_task_view()
switcher:           user.system_switcher()
clip show:          user.system_show_clipboard()
configure {user.launch_command}:
     user.exec(launch_command)
summon {user.directories}:
     user.system_open_directory(directories)