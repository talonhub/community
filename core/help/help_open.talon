tag: user.help_open
mode: command
mode: dictation
-

help next$: user.help_next()
help (previous | last)$: user.help_previous()
help <number>$: user.help_select_index(number - 1)
help return$: user.help_return()
help refresh$: user.help_refresh()
help close$: user.help_hide()
help show details$: user.help_show_details()
help hide details$: user.help_hide_details()
help key first$: user.help_key_first()
help value first$: user.help_value_first()