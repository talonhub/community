# Eye Tracking
(control | see) fusion: experimental.fusion1_toggle()
(control | see) gazing: experimental.gaze1_toggle()
(control | see) head: experimental.head1_toggle()

# Deep Clicks
(deep | deeper | further): key("ctrl-cmd-t")
layer menu: key("ctrl-cmd-l")

# Push Pixels
push up <number>:
  edit.up()
  repeat(number - 1)

push down <number>:
    edit.down()
    repeat(number - 1)

push left <number>:
    edit.left()
    repeat(number - 1)

push right <number>:
    edit.right()
    repeat(number - 1)

# Wheel Down/Up
(we down | wown) <number>:
  user.mouse_scroll_down()
  repeat(number - 1)

(we downer | downer):
    user.mouse_scroll_down_continuous()

(we up | whip) <number>:
  user.mouse_scroll_up()
  repeat(number - 1)

(we upper | whipper):
  user.mouse_scroll_up_continuous()

(lefts | tef) <number>:
  key("shift-alt-[")
  repeat(number - 1)

(rights | rye) <number>:
  key("shift-alt-]")
  repeat(number - 1)

(we out | outs): user.mouse_scroll_stop()

# Vimium
link: key("f")
link new: key("shift-f")
link copy: key("yf")

# Vimac
(fly | get): key("ctrl-f")

# Simple Shortcuts
duplicate: key("cmd-d")
clicker: key("cmd-shift-d")
grab all: key("cmd-a")

# General
(petes | peas): core.repeat_command(1)
