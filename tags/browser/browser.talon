tag: browser
-
tag(): user.navigation
tag(): user.find
tag(): user.address_bar

go home: browser.go_home()
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