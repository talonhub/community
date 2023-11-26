tag: browser
-
address bar | go address | go url: browser.focus_address()
address copy | url copy | copy address | copy url:
    browser.focus_address()
    sleep(50ms)
    edit.copy()
go home: browser.go_home()
[go] forward [<number_small>]: 
    numb  = number_small or 1
    browser.go_forward()
    repeat(numb - 1)
go (back | backward) [<number_small>]: 
    numb  = number_small or 1
    browser.go_back()
    repeat(numb - 1)
go {user.website}: browser.go(website)
go private: browser.open_private_window()
bookmark that: browser.bookmark()
bookmark tabs: browser.bookmark_tabs()
(refresh | reload) that: browser.reload()
(refresh | reload) that hard: browser.reload_hard()

bookmark show: browser.bookmarks()
bookmark bar [show]: browser.bookmarks_bar()
downloads show: browser.show_downloads()
extensions show: browser.show_extensions()
history show: browser.show_history()
cache show: browser.show_clear_cache()
dev tools [show]: browser.toggle_dev_tools()