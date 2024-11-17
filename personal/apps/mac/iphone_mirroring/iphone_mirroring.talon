app: i_phone_mirroring
-
settings():
	user.accessibility_dictation = false
	user.context_sensitive_dictation = false
home: user.menu_select('View|Home Screen')
switch: user.menu_select('View|App Switcher')
{user.phone_applications}: 
	user.menu_select('View|Spotlight')
	sleep(1000ms)
	edit.delete()
	sleep(1000ms)
	insert(phone_applications)
	sleep(1000ms)
	key(enter)
search <user.word>: 
	user.menu_select('View|Spotlight')
	sleep(1000ms)
	edit.delete()
	sleep(1000ms)
	insert(word)
search:
	user.menu_select('View|Spotlight')

access:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("25.923614501953125 -95.9691162109375 -21.60113525390625 -24.230224609375", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)