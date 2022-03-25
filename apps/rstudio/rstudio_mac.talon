os: mac
app: RStudio
-

# random QOL
set as: " = "
subtract: " - "
add: " + "
assign that:                     key("alt--")
pipe that:                       key("cmd-shift-m")

# Run code
run that:                        key("cmd-enter")
run document:                    key("cmd-alt-r")
run from top:                    key("cmd-alt-b")
run to end:                      key("cmd-alt-e")
run (function|funk):             key("cmd-alt-f")
run section:                     key("cmd-alt-t")
run previous chunks:             key("cmd-alt-p")
run chunk:                       key("cmd-alt-c")
run next chunk:                  key("cmd-alt-n")
run all:                         key("cmd-shift-s")
run knitter:                     key("cmd-shift-k")
run profiler:                    key("cmd-shift-alt-p")
run again:                       key("cmd-alt-p") #re-run prev region

# text selection/navigation
paint <user.arrow_key>:          key("shift-{arrow_key}")
select that:                     key("cmd-alt-shift-m") # selects whole symbol; if number/math symbol, etc. moves to left
select (inside|args):      key("ctrl-shift-e")
matching (brace|paren):          key("ctrl-p")
expand select:                   key("shift-alt-cmd-up")
shrink select:                   key("shift-alt-cmd-down")

navigate|jump) back:             key("cmd-f9")
(navigate|jump) forward:         key("cmd-f10")
indent that:                     key("cmd-i") #auto-indent, just use tab for normal indents
indent remove:                   key("shift-tab")
go line up:                      key("alt-up")
go line down:                    key("alt-down")
go line number:                  key("cmd-shift-alt-g")
(dupe|duplicate) line up:        key("cmd-alt-up")
(dupe|duplicate) line [down]:    key("cmd-alt-down")
move line up:                    key("alt-up")
move line down:                  key("alt-down") 

(copy|yank) before:              key("ctrl-u") # yanks line up to cursor
(copy|yank) after:               key("ctrl-k") #yanks line after cursor
push that:                       key("ctrl-y") #inserts currently yanked text

jump to:                         key("cmd-shift-opt-j") #section/function navigator
add cursor up:                   key("ctrl-alt-up")
add cursor down:                 key("ctrl-alt-down")
move active cursor up:           key("ctrl-alt-shift-up")
move active cursor down:         key("ctrl-alt-shift-down")
split that:                      key("ctrl-alt-a") # multi cursors split into lines.

extract as (function|funk):      key("cmd-alt-x")
extract as (variable|var):       key("cmd-alt-v")

section new:                     key("cmd-shift-r") #section header

# folding
fold that:                       key("cmd-alt-l")
unfold that:                     key("cmd-shift-alt-l")
fold all:                        key("cmd-alt-o")
unfold all:                      key("cmd-shift-alt-o")

# find and replace
finder:                          key("cmd-f")
find text <user.text>:
    key("cmd-f")
    insert(text or "")
find that:                       key("cmd-e") #find selected text
find next:                       key("cmd-g")
find previous:                   key("cmd-shift-g")
replace those:                   key("cmd-shift-j")
# theoretically you're supposed to be able to select "in selection"
# in the finder but it's not working for me; 
file find:                       key("cmd-shift-f")
check spelling:                  key("f7")

# format
comment that:                    key("cmd-shift-c")
reflow comment:                  key("ctrl-shift-/")
format that:                     key("ctrl-shift-a")

# delete
delete line:                     key("cmd-d")
delete word left:                key("alt-backspace")
delete word right:               key("alt-delete"))
delete after:                    key("ctrl-k") #delete to end of line
insert knitter chunk:            key("cmd-alt-i")

# panel/tab navigation
go source:                       key("ctrl-1")
go console:                      key("ctrl-2")
go to help:                      key("ctrl-3")
go to history:                   key("ctrl-4")
go to files:                     key("ctrl-5")
go to (plots|plot):              key("ctrl-6")
go to packages:                  key("ctrl-7")
go to environment:               key("ctrl-8")
go to git:                       key("ctrl-9")
go to build:                     key("ctrl-0")
go to terminal:                  key("alt-shift-t")
go to omni:                      key("ctrl-.")
go to line:                      key("cmd-shift-alt-g")
go to section:                   key("cmd-shift-alt-j")
go to tab:                       key("ctrl-shift-.")
tab (previous|back|pree):        key("ctrl-f11")
tab next:                        key("ctrl-f12")
tab first:                       key("ctrl-shift-f11")
tab last:                        key("ctrl-shift-f12")
tab new:                         key("cmd-shift-n") 
tab save:                        key("cmd-s")
tab save all:                    key("cmd-alt-s")
tab save as:                     key("cmd-shift-s") ## Custom shortcut
tab close all:                   key("cmd-shift-w")

# session
session force kill:              key("ctrl-shift-c") ## Custom shortcut
session new:                     key("ctrl-shift-n") 
session quit:                    key("cmd-q")
session restart:                 key("cmd-shift-f10")
zoom source:                     key("ctrl-shift-1")
(zoom|show) all:                 key("ctrl-shift-0")

# termal stuff
terminal new:                    key("shift-alt-t")

#help/definitions
help that:                       key("f1")
define that:                     key("f2")

#plots
plot (previous|back|pree):       key("cmd-alt-f11")
plot next:                       key("cmd-alt-f12")
plot save:                       key("ctrl-alt-shift-s") ## Custom shortcut

# terminal
rename current terminal:       key("shift-alt-r")
clear current terminal:        key("ctrl-shift-l")
terminal previous:             key("ctrl-alt-f11")
terminal next:                 key("ctrl-alt-f12")
send to terminal:              key("cmd-alt-enter") #send current line

# devtools, package development, and session management
dev tools build:                 key("cmd-shift-b")
dev tools load all:              key("cmd-shift-l")
dev tools test:                  key("cmd-shift-t")
dev tools check:                 key("cmd-shift-e")
dev tools document:              key("cmd-shift-d")

# Debugging
toggle breakpoint:               key("shift-f9")
debug next:                      key("f10")
debug step into (function|funk): key("shift-f4")
debug finish (function|funk):    key("shift-f6")
debug continue:                  key("shift-f5")
debug stop:                      key("shift-f8")

# Git/SVN
run git diff:                    key("ctrl-alt-d")
run git commit:                  key("ctrl-alt-m")

# 

# Other shortcuts that could be enabled
# run line and stay:             key("alt-enter")
# run and echo all:              key("cmd-shift-enter")
# clear console:                 key("ctrl-l")
# popup history:                 key("cmd-up")
# change working directory:      key("ctrl-shift-h")
# new document (chrome only):    key("cmd-shift-alt-n")
# scroll diff view:              key("ctrl-up/down")
# sync editor & pdf preview:     key("cmd-f8")
