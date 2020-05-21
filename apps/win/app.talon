os: windows
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
	
action(app.window_next): 
	key(alt:down)
	key(tab)

action(app.window_previous): 
	key(alt:down)
	key(shift-tab)

action(user.window_last):
	key(alt-tab)

action(user.window_select):
	key(enter)
	key(alt:up)

action(app.window_hide_others):
	key(win-d alt-tab)
	

action(app.window_open):
	key(ctrl-n)

action(user.window_maximize):
	key(super-up)

action(user.window_minimize):
	key(super-down)

action(user.window_move_left_screen):
	key(super-shift-left)

action(user.window_move_right_screen):
	key(super-shift-right)

action(user.window_snap_left):
	key(super-left)

action(user.window_snap_right):
	key(super-right)

	