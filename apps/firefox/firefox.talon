app: firefox
-
tag(): browser
tag(): user.tabs

tab search:
    browser.focus_address()
    insert("% ")
tab search <user.text>$:
    browser.focus_address()
    insert("% {text}")
    key(down)

(sidebar | panel) bookmarks: user.firefox_bookmarks_sidebar()
(sidebar | panel) history: user.firefox_history_sidebar()
