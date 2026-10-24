tag: user.community_settings_window
-

settings hide: user.settings_window_hide()
page {user.community_settings_window_page}:
    user.settings_window_open(community_settings_window_page)
setting {user.community_settings_window_setting}:
    user.settings_window_choose_setting_ui(community_settings_window_setting)
comment toggle {user.community_settings_window_setting}:
    user.settings_window_toggle_commenting_setting(community_settings_window_setting)
