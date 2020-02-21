os: windows

#i don't see a need to restrict the app here, this just defines the actions
#each app can support appropriate voice commands as needed
#the below are for 1password, redefine as needed
-
action(user.knausj_talon.code.password_manager.password_fill):
	key(ctrl-\\)

action(user.knausj_talon.code.password_manager.password_show):
	key(alt-ctrl-\\)
	
action(user.knausj_talon.code.password_manager.password_new):
	key(ctrl-n)
	
action(user.knausj_talon.code.password_manager.password_duplicate):
	key(ctrl-d)
	
action(user.knausj_talon.code.password_manager.password_edit):
	key(ctrl-e)
	
action(user.knausj_talon.code.password_manager.password_delete):
	key(ctrl-delete)

