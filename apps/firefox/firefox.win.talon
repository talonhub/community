os: windows
app: firefox
-
tag(): browser
tag(): user.tabs

action(app.tab_next): key(ctrl-pagedown)
action(app.tab_previous): key(ctrl-pageup)

#action(browser.address):

action(browser.bookmark):
	key(ctrl-d)

action(browser.bookmark_tabs):
	key(ctrl-shift-d)
	
action(browser.bookmarks):
	key(ctrl-shift-b)
  
action(browser.bookmarks_bar):
	key(alt-v)
	sleep(50ms)
	key(t)
	sleep(50ms)
	key(b)

action(browser.focus_address): 
	key(ctrl-l)
	
#action(browser.focus_page):

action(browser.focus_search):
	browser.focus_address()

action(browser.go):
	browser.focus_address()
	insert(url)
	key(enter)

action(browser.go_blank):
	key(ctrl-n)
	
action(browser.go_back):
	key(alt-left)

action(browser.go_forward):
	key(alt-right)
	
action(browser.go_home):
	key(alt-home)

action(browser.open_private_window):
	key(ctrl-shift-p)

action(browser.reload):
	key(ctrl-r)

action(browser.reload_hard):
	key(ctrl-shift-r)

#action(browser.reload_hardest):
	
action(browser.show_clear_cache):
	key(ctrl-shift-delete)
  
action(browser.show_downloads):
	key(ctrl-j)

action(browser.show_extensions):
	key(ctrl-shift-a)

action(browser.show_history):
	key(ctrl-h)
	
action(browser.submit_form):
	key(enter)

#action(browser.title)

action(browser.toggle_dev_tools):
	key(ctrl-shift-i)
