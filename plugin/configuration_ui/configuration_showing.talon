tag: user.community_settings_window
-

settings hide: user.settings_window_hide()
page {user.community_settings_window_page}:
    user.settings_window_open(community_settings_window_page)
setting <number>: user.settings_window_choose_setting_ui(number)
comment toggle <number>: user.settings_window_toggle_commenting_setting(number)
