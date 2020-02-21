os: mac

#i don't see a need to restrict the app here, this just defines the actions
#each app can support appropriate voice commands as needed
#the below are for 1password, redefine as needed
-
action(user.knausj_talon.actions.password_manager.password_fill):
	key(cmd-\\)

action(user.knausj_talon.actions.password_manager.password_show):
	key(alt-cmd-\\)
	
action(user.knausj_talon.actions.password_manager.password_new):
	key(cmd-n)
	
action(user.knausj_talon.actions.password_manager.password_duplicate):
	key(cmd-d)
	
action(user.knausj_talon.actions.password_manager.password_edit):
	key(cmd-e)
	
action(user.knausj_talon.actions.password_manager.password_delete):
	key(cmd-delete)

