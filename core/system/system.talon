^(screen | screens) off$: user.system_switch_screen_power(false)
(screen | screens) on: user.system_switch_screen_power(true)

system (settings | preferences | prefs): user.system_show_settings()

^system lock$: user.system_lock()
^system exit$: user.system_show_exit_menu()
