#custom eclipse commands go here
app: eclipse
-
tag(): user.find_and_replace
tag(): user.line_commands
# tag(): user.multiple_cursors
tag(): user.splits
tag(): user.tabs
# splits.py support end

please [<user.text>]:
    key(ctrl-3)
    insert(user.text or "")

# Sidebar
bar explore: key(alt-shift-w p)
# bar extensions:
bar outline: key(alt-shift-q o)

# bar run:

# bar source:
# bar switch:

# Panels
# panel control:
panel output:
    key(alt-shift-q)
    sleep(200ms)
    key(c)
panel problems:
    key(alt-shift-q)
    sleep(200ms)
    key(x)
panel errors:
    key(alt-shift-q)
    sleep(200ms)
    key(l)
panel breakpoints:
    key(alt-shift-q)
    sleep(200ms)
    key(b)
panel search:
    key(alt-shift-q)
    sleep(200ms)
    key(s)
panel variables:
    key(alt-shift-q)
    sleep(200ms)
    key(v)
# panel switch:
# panel terminal:

# Settings
show settings: key(alt-w p)
show shortcuts: key(ctrl-shift-l)
#show snippets:

# Display
# centered switch:
# fullscreen switch:
# theme switch:
# wrap switch:
# zen switch:

# File Commands
file hunt [<user.text>]:
    key(ctrl-shift-r)
    sleep(50ms)
    insert(text or "")
# file copy path:
# file create sibling:
file create: key(ctrl-n)
file open folder: key(alt-shift-w x)
file rename: key(alt-shift-w p enter f2)
file reveal: key(alt-shift-w p enter)

# Language Features
# suggest show:
# hint show:
# definition show:
# definition peek:
# definition side:
# references show:
# references find:
# format that:
# format selection:
imports fix: key(ctrl-shift-o)
# problem last:
# problem fix:
# rename that:
# refactor that:
# whitespace trim:
# language switch:
refactor rename: key(alt-shift-r)
refactor this: key(alt-shift-i)

#code navigation
(go declaration | follow): key(f3)
go back: key(alt-left)
go forward: key(alt-right)
# go implementation:
# go recent:
# go type:
# go usage:

# Bookmarks.
#requires https://marketplace.eclipse.org/content/quick-bookmarks
go marks: key(alt-end)
toggle mark: key(ctrl-alt-b down enter)
go next mark: key(alt-pagedown)
go last mark: key(alt-pageup)

# Folding
# fold that:
# unfold that:
# fold those:
# unfold those:
# fold all:
# unfold all:
# fold comments:

#Debugging
break point: key(ctrl-shift-b)
step over: key(f6)
debug step into: key(f5)
debug step out [of]: key(f7)
#debug start: user.vscode("workbench.action.debug.start")
#debug pause:
#debug stopper:
debug continue: key(f8)
#debug restart:

# Terminal
# terminal external: user.vscode("workbench.action.terminal.openNativeConsole")

# terminal new: user.vscode("workbench.action.terminal.new")
# terminal next: user.vscode("workbench.action.terminal.focusNextPane")
# terminal last:user.vscode("workbench.action.terminal.focusPreviousPane")
# terminal split: user.vscode("workbench.action.terminal.split")
# terminal trash: user.vscode("Terminal:Kill")
# terminal scroll up: user.vscode("Terminal:ScrollUp")
# terminal scroll down: user.vscode("Terminal:ScrollDown")

#TODO: should this be added to linecommands?
copy line down: key(ctrl-alt-down)
copy line up: key(ctrl-alt-up)
