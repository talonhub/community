app: firefox
-
tag(): browser
tag(): user.tabs
tag(): user.vimium
tab search:
    browser.focus_address()
    insert("% ")
tab search <user.text>$:
    browser.focus_address()
    insert("% {text}")
    key(down)
