os: windows
os: linux
-
#app.preferences()

action(app.tab_close):
	key(ctrl-w)
	
#action(app.tab_detach):
#  Move the current tab to a new window
  
action(app.tab_next):
	key(ctrl-tab)
	
action(app.tab_open):
	key(ctrl-t)
	
action(app.tab_previous):
	key(ctrl-shift-tab)
	
action(app.tab_reopen):
	key(ctrl-shift-t)
	
action(app.window_close):
	key(alt-f4)
	
action(app.window_hide):
	key(alt-space n)
	
action(app.window_hide_others):
	key(win-d alt-tab)
	
#requires easy window switcher or equivalent (built into most Linux)
action(app.window_next): 
	key(alt-`)

action(app.window_open):
	key(ctrl-n)

#requires easy window switcher or equivalent (built into most Linux)
action(app.window_previous): 
	key(alt-shift-`)
