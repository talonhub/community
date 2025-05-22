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

### Novel split commands: ###

# Create a new split in the current split's working directory.
# (Requires RPC)
split window here: user.split_window_here()

# Go to the most recently-used split
# (Requires RPC)
split switch: user.split_switch()

# Move to the split in the given direction.
# (Requires RPC)
go split <user.arrow_key>: user.split_relative(arrow_key)

# Start kitty's interactive window chooser.
# Choose the split by "pressing" the number overlaid on the split you want.
split choose: user.split_choose()

### Miscellaneous commands: ###

# Start a command line to run a kitten.
kitten <user.text>: user.kitten_insert(text)
