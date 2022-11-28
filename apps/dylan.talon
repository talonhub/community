# Eye Tracking
(control | see) fusion: experimental.fusion1_toggle()
(control | see) gazing: experimental.gaze1_toggle()
(control | see) head: experimental.head1_toggle()
(control | see) eyes: tracking.control_toggle()

# Deep Clicks
deep: key("ctrl-cmd-t")

(deeper | further):
    key("ctrl-cmd-t")
    mouse_click()
	  mouse_click()

# Insane Click Into
(deepest | dive in | dive):
    key("cmd")
    mouse_click()
    mouse_click()
    mouse_click()
    mouse_click()
    mouse_click()
    mouse_click()
    mouse_click()
    mouse_click()
    mouse_click()
    mouse_click()

# Insane Paste Click Into
replace:
  key("cmd")
  mouse_click()
  mouse_click()
  mouse_click()
  mouse_click()
  mouse_click()
  mouse_click()
  mouse_click()
  mouse_click()
  mouse_click()
  key("enter")
  sleep(200ms)
  edit.select_all()  
  edit.paste()

# Triple click
flock:
    mouse_click()
	  mouse_click()
    mouse_click()

# Quad click
quad:
  mouse_click()
  mouse_click()
  mouse_click()
  mouse_click()

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
(we down | dao) <number>:
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

outs: user.mouse_scroll_stop()

# Vimium
#link: key("f")
#link new: key("shift-f")
#link copy: key("yf")

# Vimac
get: key("ctrl-f")

# Vim Motion
moe: key("cmd-;")

# Shortcat
cliff <user.letter>:
  key("cmd-shift-`")
  sleep(200ms)
  insert(letter)

cling <user.text>:
  key("cmd-shift-`")
  sleep(200ms)
  insert(text)

climb <user.text>:
  key("cmd-shift-`")
  sleep(200ms)
  insert(text)
  sleep(200ms)
  key("enter")

top <user.letter>:
  key("ctrl-{letter}")

toll <user.letter>:
  key("ctrl-{letter} enter")

# Simple Shortcuts
(duplicate | duce): key("cmd-d")
(clicker | clicks): key("cmd-shift-d")
grab all: key("cmd-a")

# Sentence Input
zee <user.text>:
  insert(user.formatted_text(text, "CAPITALIZE_FIRST_WORD"))

# Clear all and Replace with Sentence 
sent <user.text>:
  edit.select_all()
  edit.delete()
  sleep(200ms)
  insert(user.formatted_text(text, "CAPITALIZE_FIRST_WORD"))

# Clear all and Replace with Titles 
lose <user.text>:
    edit.select_all()
    edit.delete()
    sleep(200ms)
    insert(user.formatted_text(text, "CAPITALIZE_ALL_WORDS"))

# Click into, select all, clear and Replace with Titles 
blew <user.text>:
  mouse_click(0)
  key("enter")
  edit.select_all()
  edit.delete()
  sleep(200ms)
  insert(user.formatted_text(text, "CAPITALIZE_ALL_WORDS"))

# Copy, paste, enter and delete
(coffee | crop): edit.copy()
(pasta | path): edit.paste()

# Select all delete and then paste
clear paste:
    edit.select_all()
    edit.delete()
    edit.paste()

# Click on words select all delete and paste
(stacy | hap):
    mouse_click(0)
    key("enter")
    edit.select_all()
    edit.delete()
    edit.paste()

# Double click and select all to copy
scold:
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    edit.select_all()
    edit.copy()

# Double click then copy
grab:
  mouse_click(0)
  mouse_click(0)
  edit.copy()

# Select all and then copy
coals:
    edit.select_all()
    edit.copy()

# Multi select by doing shift click
stick:
    key("shift:down")
    mouse_click(0)
    key("shift:up")

# Command individual select objects and open link new tab
(strike | linker | link new | lynx):
    key("cmd:down")
    mouse_click(0)
    key("cmd:up")

# Alt mouse click
alt:
  key("alt:down")
  mouse_click(0)
  key("alt:up")

# Enter key
drop [<number>]:
    key("enter")
    repeat(number - 1)

# Delete key
dellz [<number>]:
    key("backspace")
    repeat(number - 1)

# General
(petes | peas): core.repeat_command(1)
sequel: " = "
quit this: key("cmd-q")

# Emoji
emoji:
  key("cmd-ctrl-space")
  
# Open slack and go to all unreads
slack feed: key(cmd-alt-2)

# Open Work Email
avant mail: key("alt-cmd-1")

# Measuring with alt key
mease in: key(alt:down)
mease out: key(alt:up)

# Duplicate and drag
dupes:
  key(alt:down)
  mouse_drag(0)
  sleep(3500ms)
  key(alt:up)

# Drag
# da: mouse_drag(0)

# Double Click Drag
dag:
  mouse_drag(0)
  mouse_drag(0)

# Add an asterik with a space
spaz: " *"

# Add an ... with a space
three dot: " ..."

# Add an / with a space between
nex: " / "


# Webflow
quickie: key("cmd-k")

# zoom 
zoomer: user.mouse_trigger_zoom_mouse()

# Focus Figma
(go fig | figz): "focus figma"


beep:
  mouse_click()
  mouse_click()
  mouse_click()
  mouse_click()
  sleep(200ms)
  key("cmd-c")

heat:
    mouse_click()
    mouse_click()
    mouse_click()
    sleep(200ms)
    key("alt-shift-cmd-v")
