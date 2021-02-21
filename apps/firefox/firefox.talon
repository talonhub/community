app: firefox
-
tag(): browser
tag(): user.tabs

# TODO
#action(browser.address):
#action(browser.title):

action(browser.go):
	browser.focus_address()
	insert(url)
	key(enter)

action(browser.focus_search):
	browser.focus_address()

action(browser.submit_form):
	key(enter)
