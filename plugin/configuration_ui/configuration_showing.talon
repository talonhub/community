tag: user.community_settings_window
-

configuration hide: user.hide_configuration_window()
page {user.community_settings_window_page}:
    user.configuration_window_open_page(community_settings_window_page)
setting {user.community_settings_window_setting}:
    user.configuration_window_choose_setting_ui(community_settings_window_setting)
comment toggle {user.community_settings_window_setting}:
    user.configuration_window_toggle_commenting_setting(community_settings_window_setting)
