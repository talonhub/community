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
  sleep(10ms)
  insert("% ")
tab search <user.text>$:
  browser.focus_address()
  sleep(10ms)
  insert("% {text}")
  sleep(10ms)
  key(down)

