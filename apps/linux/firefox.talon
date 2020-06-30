os: linux
app: Firefox
app: firefox
-
tag(): browser
tag(): firefox
tag(): tabs

#action(browser.address):

action(browser.bookmark):
	key(ctrl-d)

action(browser.bookmark_tabs):
	key(ctrl-shift-d)

action(browser.bookmarks):
	key(ctrl-shift-o)

action(browser.bookmarks_bar):
	key(ctrl-b)

action(browser.focus_address):
	key(ctrl-l)

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
	key(ctrl-shift-del)

action(browser.show_downloads):
	key(ctrl-shift-y)

action(browser.show_extensions):
	key(ctrl-shift-a)

action(browser.show_history):
	key(ctrl-h)

action(browser.submit_form):
	key(enter)

#action(browser.title)

action(browser.toggle_dev_tools):
	key(ctrl-shift-i)
