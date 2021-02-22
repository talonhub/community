app: firefox
-
tag(): browser
tag(): user.tabs

# TODO
#action(browser.address):
#action(browser.title):

action(browser.focus_search):
	browser.focus_address()

action(browser.submit_form):
	key(enter)

tab search:
  browser.focus_address()
  insert("% ")
tab search <user.text>$:
  browser.focus_address()
  insert("% {text}")
  key(down)

