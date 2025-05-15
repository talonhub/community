app.exe: kitty
app.name: kitty
-

# Kitty is a terminal emulator for Unix systems (including WSL, unofficially).
# Learn more at https://sw.kovidgoyal.net.

tag(): terminal
tag(): user.generic_unix_shell
tag(): user.unix_utilities
tag(): user.readline
tag(): user.git

# Cribbed from the .talon file for iTerm
suspend: key(ctrl-z)
resume:
    insert("fg")
    key(enter)
resume [<user.number_string>]:
    insert("fg " + number_string)
    key(enter)


# Overrides for basic editing, tab, and window management.
# Note that if your `kitty_mod` is set to something other than the default of
# ctrl-shift, you will need to make the same change here.
# Note that some window managers (particularly GNOME3) may have conflicts with
# some key combos

copy that: key(ctrl-shift-c)
(pace | paste) that: key(ctrl-shift-v)

tab open: key(ctrl-shift-t)
tab next: key(ctrl-tab)
tab last: key(ctrl-shift-tab)

split window: key(ctrl-shift-enter)
# The `new_window_with_cwd` action isn't bound in a default kitty.conf
split window here: key(alt-shift-enter)
split next: key(ctrl-shift-])
split last: key(ctrl-shift-[)
# Move to the split in the given direction.
# Kitty doesn't define `neighboring_window` by default. Uncomment this and set
# it to match the binding set in your kitty.conf. N.B. that ctrl-alt tends to
# get eaten by GNOME3.
# go split <user.arrow_key>:
# 	key("ctrl:down")
# 	key("alt:down")
# 	key(arrow_key)
# 	key("ctrl:up")
# 	key("alt:up")

scroll up: key(ctrl-shift-up)
scroll down: key(ctrl-shift-down)
page up: key(ctrl-shift-pgup)
page down: key(ctrl-shift-pgdown)
