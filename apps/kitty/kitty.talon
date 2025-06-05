app: kitty
-
#
# Kitty is a terminal emulator for Unix systems (including WSL, unofficially).
# Learn more at https://sw.kovidgoyal.net.
#
# Some commands rely on your 1) kitty.conf enabling remote control, and 2) your
# Talon and kitty configs agreeing on where the unix socket is. Most commands,
# if these conditions are not met, will fall back to using the default key
# combinations; some commands do not have default key bindings. In the event
# such a command is called but RPC is not set up, you will get a desktop
# notification saying what the kitty command was and advising you to enable RPC.
#

tag(): user.splits
tag(): user.tabs
tag(): terminal
tag(): user.generic_unix_shell
tag(): user.unix_utilities
tag(): user.readline
tag(): user.git

### Novel split commands: ###

# Start kitty's interactive window chooser.
# Choose the split by "pressing" the number overlaid on the split you want.
split choose: user.split_choose()

# Move to the split in the given relative/arrow direction.
# (Requires RPC)
go split <user.arrow_key>: user.split_relative(arrow_key)

# Go to the most recently-used split
# (Requires RPC)
split switch: user.split_switch()

# Create a new split in the current split's working directory.
# (Requires RPC)
split window here: user.split_window_here()

### Novel tab commands: ###

# Start kitty's interactive tab chooser.
# Choose the tab by "pressing" the number of the tab you want.
tab choose: user.tab_choose()
#
# Go to the most recently-used split
# (Requires RPC)
tab switch: user.tab_switch()

### Miscellaneous commands: ###

# Start a command line to run a kitten.
kitten <user.text>: user.kitten_insert(text)

# Hints kitten
# https://sw.kovidgoyal.net/kitty/kittens/hints/
# In short, similar idea to Cursorless, the draft plugin, Tridactyl, Vimium, etc.
# (These should all work without RPC unless you have rebound kitty_mod+p.)
hint U R L: user.hint_url()
hint hash: user.hint_hash()
hint line: user.hint_line()
hint line clip: user.hint_line_clip()
# Like 'hint line', but copy it to the clipboard instead of the command line.
hint line in file: user.hint_line_in_file()
hint path: user.hint_path_insert()
hint path clip: user.hint_path_clip()
# Like 'hint path', but open the file with the default program instead of paste it
# to the command line.
hint path open: user.hint_path_open()
hint word: user.hint_word()
hint word clip: user.hint_word_clip()
hint terminal link: user.hint_terminal_link()
