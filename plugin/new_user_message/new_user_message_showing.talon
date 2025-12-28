tag: user.new_user_message_showing
-

message hide: user.new_user_message_hide()

message dismiss:
	user.new_user_message_stop_showing_on_startup()
	user.new_user_message_hide()