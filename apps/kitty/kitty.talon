app: kitty
-

# Kitty is a terminal emulator for Unix systems (including WSL, unofficially).
# Learn more at https://sw.kovidgoyal.net.

# Cribbed from the .talon file for iTerm
suspend: key(ctrl-z)
resume:
    insert("fg")
    key(enter)
resume [<user.number_string>]:
    insert("fg " + number_string)
    key(enter)

# The `new_window_with_cwd` action isn't bound in a default kitty.conf
# (but it's highly recommended!)
split window here: key(alt-shift-enter)
# Move to the split in the given direction.
# Kitty doesn't define `neighboring_window` by default. Uncomment this and set
# it to match the binding set in your kitty.conf. N.B. that ctrl-alt tends to
# get eaten by GNOME3.
# go split <user.arrow_key>:
#   key("ctrl:down")
#   key("alt:down")
#   key(arrow_key)
#   key("ctrl:up")
#   key("alt:up")
