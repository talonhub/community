# While a right-click menu is open in the thumbnail switcher. Numbers (bare or with
# "pick") run the menu's numbered items; the switcher's own number commands for tiles
# do nothing until the menu closes, except "menu <number>".
os: windows
tag: user.thumbnail_switcher_menu_open
-
back: user.thumbnail_switcher_menu_back()
menu close: user.thumbnail_switcher_close_menu()
# In a jump list: pin, unpin or remove an entry by its number.
pin <number_small>: user.thumbnail_switcher_menu_button("pin", number_small)
unpin <number_small>: user.thumbnail_switcher_menu_button("unpin", number_small)
remove <number_small>: user.thumbnail_switcher_menu_button("remove", number_small)
