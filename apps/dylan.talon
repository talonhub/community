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
get: key("ctrl-f")

# Vim Motion
moe: key("cmd-;")

# Shortcat
cliff <user.letter>:
  key("cmd-shift-space")
  sleep(200ms)
  insert(letter)

cling <user.text>:
  key("cmd-shift-space")
  sleep(200ms)
  insert(text)

climb <user.text>:
  key("cmd-shift-space")
  sleep(200ms)
  insert(text)
  sleep(200ms)
  key("enter")

top <user.letter>:
  key("ctrl-{letter}")

toll <user.letter>:
  key("ctrl-{letter} enter")

# Simple Shortcuts
duplicate: key("cmd-d")
clicker: key("cmd-shift-d")
grab all: key("cmd-a")

# Clear all and Replace word 
lose <user.text>:
    edit.select_all()
    edit.delete()
    sleep(200ms)
    insert(user.formatted_text(text, "CAPITALIZE_ALL_WORDS"))

ant: key("enter")
dellz: key("delete")

# General
(petes | peas): core.repeat_command(1)
sequel: " = "
