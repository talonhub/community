# Usage:
#  - See doc/vim.md
#  - See code/vim.py
#
# Where applicable I try to explicitly select appropriate API for terminal
# escaping, etc. However in cases where it is unlikely you will say a command
# from terminal mode, I don't bother. Example "save file" doesn't have
# explicit terminal escaping.

# ToDo:
#  - new terminal buffer command
#  - specify specific buffer into split
#  - add support for moving buffer to tabs
#  - support more clearing of queued vim commands, ex: go to line, etc
#  - add an insert command for just saying text and force to insert mode
#  - consider making go mandatory for buffer and tab switching
#  - add support for relative line jumping
#  - more automatic highlighting, for example:
#     `highlight 2 above` should visual line select two lines above current.
#     especially useful when inside vim terminal using gdb, etc
#     `highlight X lines @ [line] NNNN`
#     `yank X lines @ [line] NNNN`
#     `yank last X lines` (relative reverse copy)
#     `yank next X lines` (relative forward copy)

os:linux
app:gvim
app:/term/
and win.title:/VIM/
-

tag(): vim
settings():
    # Whether or not to always revert back to the previous mode. Example, if
    # you are in insert mode and say 'delete word' it will delete one word and
    # keep you in insert mode. Same as ctrl-o in VIM.
    user.vim_preserve_insert_mode = 1

    # Whether or not to automatically adjust modes when using commands. Example
    # saying "go line 50" will first switch you out of INSERT into NORMAL and
    # then jump to the line. Disabling this setting would put :50\n into your
    # file if said "go line 50" while in INSERT mode.
    user.vim_adjust_modes = 1

    # Select whether or not talon should dispatch notifications on mode changes
    # that are made. Not yet completed, as notifications are kind of wonky on
    # Linux
    user.vim_notify_mode_changes = 0

    # Whether or not all commands that transfer out of insert mode should
    # automatically escape out of terminal mode. Turning this on is quite
    # troublesome.
    user.vim_escape_terminal_mode = 0

    # When issuing counted actions in vim you can prefix a count that will,
    # however the existing talon grammar already allows you to utter a number,
    # so we want to cancel any existing counts that might already by queued in
    # vim in error. This also helps prevent accidental number queueing if talon
    # mishears a command such as "delete line" as "delete" "nine". Without this
    # setting, if you then said "undo" it would undo the last 9 changes, which
    # is annoying.
    #
    # This setting only applies to commands run through the actual counted
    # actions grammar itself
    user.vim_cancel_queued_commands = 1

    # When you are escaping queued commands, it seems vim needs time to recover
    # before issuing the subsequent commands. This controls how long it waits,
    # in seconds
    user.vim_cancel_queued_commands_timeout = 0.3

    # It how long to wait before issuing commands after a mode change. You
    # want adjust this if when you say things like undo from INSERT mode, an
    # "u" gets inserted into INSERT mode
    user.vim_mode_change_timeout = 0.3

###
# Actions - Talon generic_editor.talon implementation
###
#
# NOTE: You can disable generic_editor.talon by renaming it, and still fully
# control vim. These are more for people that are used to the official talon
# editor commands that want to trial vim a bit. I don't personally use most of
# the actions here, so they have not been thoroughly tested
###
action(edit.find):
    user.vim_normal_mode_exterm_key("/")
action(edit.find_next):
    user.vim_normal_mode_key("n")
action(edit.word_left):
    user.vim_normal_mode_key("b")
action(edit.word_right):
    user.vim_normal_mode_key("w")
action(edit.left):
    key(left)
action(edit.right):
    key(right)
action(edit.up):
    key(up)
action(edit.down):
    key(down)
action(edit.line_start):
    user.vim_normal_mode_key("^")
action(edit.line_end):
    user.vim_normal_mode_key("$")
action(edit.file_end):
    user.vim_normal_mode_key(G)
action(edit.file_start):
    user.vim_normal_mode("gg")
action(edit.page_down):
    user.vim_normal_mode_exterm_key("ctrl-f")
action(edit.page_up):
    user.vim_normal_mode_exterm_key("ctrl-b")

action(edit.extend_line_end):
    user.vim_visual_mode("$")
action(edit.extend_left):
    user.vim_visual_mode("h")
action(edit.extend_right):
    user.vim_visual_mode("l")
action(edit.extend_line_up):
    user.vim_visual_mode("k")
action(edit.extend_line_down):
    user.vim_visual_mode("j")
action(edit.extend_word_left):
    user.vim_visual_mode("b")
action(edit.extend_word_right):
    user.vim_visual_mode("w")
action(edit.extend_line_start):
    user.vim_visual_mode("^")
action(edit.extend_file_start):
    user.vim_visual_mode("gg")
action(edit.extend_file_end):
    user.vim_visual_mode("G")

action(edit.indent_more):
    user.vim_normal_mode(">>")
action(edit.indent_less):
    user.vim_normal_mode("<<")
action(edit.delete_line):
    user.vim_normal_mode("dd")
action(edit.delete):
    user.vim_normal_mode_key(x)

# note these are for mouse highlighted copy/paste. shouldn't be used for actual
# vim commands
action(edit.copy):
    key(ctrl-shift-c)
action(edit.paste):
    key(ctrl-shift-v)

###
# `code/vim.py` actions based on vimspeak
###
# commands that can be triggered in visual or normal mode, and generally don't
# have counting, etc
<user.vim_normal_counted_motion_command>:
    insert("{vim_normal_counted_motion_command}")
#<user.vim_counted_command>:
#    insert("{vim_counted_command}")
<user.vim_motions_all_adjust>:
    insert("{vim_motions_all_adjust}")
<user.vim_normal_counted_action>:
    insert("{vim_normal_counted_action}")

# XXX YYY ZZZ

###
# File editing and management
###
# NOTE: using `save` alone conflicts too much with the `say`
save file:
    user.vim_normal_mode(":w\n")
save [file] as:
    key(escape)
    user.vim_normal_mode(":w ")
save all:
    user.vim_normal_mode_exterm(":wa\n")
save and (quit|close):
    user.vim_normal_mode(":wq\n")
(close|quit) file:
    user.vim_normal_mode(":q\n")

# no \n as a saftey measure
(close|quit) all:
    user.vim_normal_mode_exterm(":qa")

force (close|quit) all:
    user.vim_normal_mode_exterm(":qa!")

force (close|quit):
    user.vim_normal_mode_exterm(":q!\n")
refresh file:
    user.vim_normal_mode(":e!\n")
edit [file|new]:
    user.vim_normal_mode_exterm(":e ")
reload [vim] config:
    user.vim_normal_mode_exterm(":so $MYVIMRC\n")

# For when the VIM cursor is hovering on a path
open [this] link: user.vim_normal_mode("gx")
open this file: user.vim_normal_mode("gf")
open this file in [split|window]:
    user.vim_set_normal_mode()
    key(ctrl-w)
    key(f)
open this file in vertical [split|window]:
    user.vim_normal_mode(":vertical wincmd f\n")

(show|list) current directory: user.vim_normal_mode(":pwd\n")
change buffer directory: user.vim_normal_mode(":lcd %:p:h\n")

###
# Standard commands
###
# XXX - technically should be handled by vim.py, but need to add "ctrl" key support
redo:
    user.vim_normal_mode_key("ctrl-r")

###
# Navigation, movement and jumping
#
# NOTE: Majority of more core movement verbs are in code/vim.py
###
[(go|jump)] [to] line <number>:
    user.vim_normal_mode_exterm(":{number}\n")

[go] relative up [line] <number>:
    user.vim_normal_mode_exterm("{number}k\n")

[go] relative down [line] <number>:
    user.vim_normal_mode_exterm("{number}j\n")

matching: user.vim_any_motion_mode_key("%")

# jump list
show jump list: user.vim_normal_mode_exterm(":jumps\n")
clear jump list: user.vim_normal_mode_exterm(":clearjumps\n")
(prev|previous|older) jump [entry]: user.vim_normal_mode_exterm_key("ctrl-o")
(next|newer) jump [entry]: user.vim_normal_mode_exterm_key("ctrl-i")
# XXX - add jump to <id>

# ctags/symbol
(jump|dive) [to] (symbol|tag): user.vim_normal_mode_key("ctrl-]")
(pop|leave) (symbol|tag): user.vim_normal_mode_key("ctrl-t")

# scrolling and page position
(focus|orient) [on] line <number>: user.vim_normal_mode_exterm(":{number}\nzt")
center [on] line <number>: user.vim_normal_mode_exterm(":{number}\nz.")
scroll top: user.vim_normal_mode_exterm("zt")
scroll (center|middle): user.vim_normal_mode_exterm("zz")
scroll bottom: user.vim_normal_mode_exterm("zb")
scroll top reset cursor: user.vim_normal_mode_exterm("z\n")
scroll middle reset cursor: user.vim_normal_mode_exterm("z.")
scroll bottom reset cursor: user.vim_normal_mode_exterm("z ")
scroll up: user.vim_normal_mode_exterm_key("ctrl-y")
scroll down: user.vim_normal_mode_exterm_key("ctrl-e")
page down: user.vim_normal_mode_exterm_key("ctrl-f")
page up: user.vim_normal_mode_exterm_key("ctrl-b")
half [page] down: user.vim_normal_mode_exterm_key("ctrl-d")
half [page] up: user.vim_normal_mode_exterm_key("ctrl-u")

###
# Text editing, copying, and manipulation
###

change remaining line: user.vim_normal_mode_key("C")
change line: user.vim_normal_mode("cc")
# XXX - this might be suited for some automatic motion thing in vim.py
swap characters: user.vim_normal_mode("xp")
swap words: user.vim_normal_mode("dwwP")
swap lines: user.vim_normal_mode("ddp")
swap paragraph: user.vim_normal_mode("d}}p")
replace <user.any>: "r{any}"
replace (ship|upper|upper case) <user.letters>:
    user.vim_normal_mode_key("r")
    user.keys_uppercase_letters(letters)

# indenting
(shift|indent) right: user.vim_normal_mode(">>")
indent [line] <number> through <number>$: user.vim_normal_mode(":{number_1},{number_2}>\n")
(shift|indent) left: user.vim_normal_mode("<<")
unindent [line] <number> through <number>$: user.vim_normal_mode(":{number_1},{number_2}>\n")


# XXX - this doesn't work with numbers below nine, because the nine will
# trigger its own discrete command in the first part of the command will
# trigger the dd below. we probably need to come up with different trigger for
# the one were you specify the line

# deleting
delete remaining [line]: user.vim_normal_mode_key("D")
delete line [at|number] <number>$: user.vim_normal_mode(":{number}d\n")
delete (line|lines) [at|number] <number> through <number>$: user.vim_normal_mode(":{number_1},{number_2}d\n")

# insert mode only
clear line: key(ctrl-u)

# copying
(copy|yank) line (at|number) <number>$: user.vim_normal_mode_exterm(":{number}y\n")
(copy|yank) line (at|number) <number> through <number>: user.vim_normal_mode_exterm(":{number_1},{number_2}y\n")

# duplicating
# XXX - these don't preserve INSERT atm because they use multiple commands
(duplicate|paste) line <number> on line <number>$: user.vim_normal_mode_np(":{number_1}y\n:{number_2}\np")
(duplicate|paste) line (at|number) <number> through <number>$: user.vim_normal_mode_np(":{number_1},{number_2}y\np")
(duplicate|paste) line <number>$: user.vim_normal_mode_np(":{number}y\np")

(dup|duplicate) line: user.vim_normal_mode_np("Yp")

# start ending at end of line
push line:
    user.vim_normal_mode_key("A")

# start ending at end of file
push file:
    user.vim_normal_mode_np("Go")

# helpful for fixing typos or bad lexicons that miss a character
inject <user.any> [before]:
    user.vim_insert_mode("{any}")
    # since there is no ctrl-o equiv coming from normal
    key(escape)

inject <user.any> after:
    user.vim_normal_mode("a{any}")
    # since we can't perserve mode with ctrl-o
    key(escape)

# XXX - look into how this works
filter line: "=="

# XXX - could preserve INSERT if swapped into two calls
[add] gap above:
    user.vim_normal_mode_np(":pu! _\n:'[+1\n")
[add] gap below:
    user.vim_normal_mode_np(":pu _\n:'[-1\n")

# XXX - This should be a callable function so we can do things like:
#       'swap on this <highlight motion>'
#       'swap between line x, y'
# assumes visual mode
swap (selected|highlighted):
    insert(":")
    # leave time for vim to populate '<,'>
    sleep(50ms)
    insert("s///g")
    key(left)
    key(left)
    key(left)

sort (selected|highlighted):
    insert(":")
    # leave time for vim to populate '<,'>
    sleep(50ms)
    insert("sort\n")

# assumes visual mode
reswap (selected|highlighted):
    insert(":")
    # leave time for vim to populate '<,'>
    sleep(50ms)
    key(up)

# Selects current line in visual mode and triggers a word swap
swap [word] on [this] line:
    key(V)
    insert(":")
    sleep(50ms)
    insert("s///g")
    key(left)
    key(left)
    key(left)

# assumes visual mode
deleted selected empty lines:
    insert(":")
    # leave time for vim to populate '<,'>
    sleep(50ms)
    insert("g/^$/d\j")

swap global:
    user.vim_normal_mode(":%s///g")
    key(left)
    key(left)
    key(left)

# XXX - should explicitly call terminal-escaping method
###
# Buffers
###
((buf|buffer) list|list (buf|buffer)s): user.vim_normal_mode_exterm(":ls\n")
(buf|buffer) (close|delete) <number>: user.vim_normal_mode_exterm(":bd {number} ")
(close|delete) (buf|buffer) <number>: user.vim_normal_mode_exterm(":bd {number} ")
(buf|buffer) close current: user.vim_normal_mode(":bd\n")
(delete|close) (current|this) buffer: user.vim_normal_mode_exterm(":bd\n")
force (buf|buffer) close: user.vim_normal_mode_exterm(":bd!\n")
(buf|buffer) open: user.vim_normal_mode_exterm(":b ")
[go] (buf|buffer) (first|rewind): user.vim_normal_mode_exterm(":br\n")
[go] (buf|buffer) (left|prev): user.vim_normal_mode_exterm(":bprev\n")
[go] (buf|buffer) (right|next): user.vim_normal_mode_exterm(":bnext\n")
[go] (buf|buffer) flip: user.vim_normal_mode_exterm(":b#\n")
[go] (buf|buffer) last: user.vim_normal_mode_exterm(":bl\n")
close (bufs|buffers): user.vim_normal_mode_exterm(":bd ")
[go] (buf|buffer) <number>: user.vim_normal_mode_exterm(":b {number}\n")

###
# Splits
###
# creating splits
new [horizontal] split:
    # XXX - until we have key combo support
    user.vim_set_normal_mode_exterm()
    key("ctrl-w")
    key(s)
new (vertical|v) split:
    # XXX - until we have key combo support
    user.vim_set_normal_mode_exterm()
    key("ctrl-w")
    key(v)
split (close|quit):
    # XXX - until we have key combo support
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(q)

new empty [horizontal] split:
    user.vim_normal_mode_exterm(":new\n")
new empty (vertical|v) split:
    user.vim_normal_mode_exterm(":vnew\n")

# navigating splits
split <user.vim_arrow>:
    # XXX - until we have key combo support
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key("{vim_arrow}")
split last:
    # XXX - until we have key combo support
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(p)
split top left:
    # XXX - until we have key combo support
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(t)
split next:
    # XXX - until we have key combo support
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(w)
split (previous|prev):
    # XXX - until we have key combo support
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(W)
split bottom right:
    # XXX - until we have key combo support
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(b)
split preview:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(P)

# personal convenience shortcuts
# split right
sprite:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(l)

# split left
speff:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(h)

# split top left
splot:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(t)

# moving windows
split (only|exclusive):
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(o)
split rotate [right]:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(r)
split rotate left:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(R)
split move top:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(K)
split move bottom:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(J)
split move right:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(L)
split move left:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(H)
split move to tab:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(T)

# window resizing
split (balance|equalize):
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(=)
split taller:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(+)
    user.vim_set_normal_mode_exterm()
split shorter:
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(-)
    user.vim_set_normal_mode_exterm()
split fatter:
    key(ctrl-w)
    key(>)
    user.vim_set_normal_mode_exterm()
split skinnier:
    key(ctrl-w)
    key(<)
set split width:
    user.vim_normal_mode_exterm(":resize ")
set split height:
    user.vim_set_normal_mode_exterm(":vertical resize ")
    insert(":vertical resize ")

###
# Diffing
###
(split|window) start diff:
    user.vim_set_normal_mode_exterm(":windo diffthis\n")

(split|window) end diff:
    user.vim_set_normal_mode_exterm(":windo diffoff\n")

buffer start diff:
    user.vim_set_normal_mode_exterm(":bufdo diffthis\n")

buffer end diff:
    user.vim_set_normal_mode_exterm(":bufdo diffthis\n")

###
# Tab
###
(list|show) tabs: user.vim_normal_mode(":tabs\n")
(close this tab|tab close): user.vim_normal_mode_exterm(":tabclose\n")
[go] tab (next|right): user.vim_normal_mode_exterm(":tabnext\n")
[go] tab (left|prev|previous): user.vim_normal_mode_exterm(":tabprevious\n")
[go] tab first: user.vim_normal_mode_exterm(":tabfirst\n")
[go] tab last: user.vim_normal_mode_exterm(":tablast\n")
[go] tab flip: user.vim_normal_mode_exterm("g\t")
[go] tab <number>: user.vim_normal_mode_exterm("{number}gt")
tab new: user.vim_normal_mode_exterm(":tabnew\n")
tab edit: user.vim_normal_mode_exterm(":tabedit ")
tab move right: user.vim_normal_mode_exterm(":tabm +\n")
tab move left: user.vim_normal_mode_exterm(":tabm -\n")

[new] tab terminal: user.vim_normal_mode_exterm(":tabe term://bash\n")

###
# Settings
###
# XXX - this is a weird edge case because we actually probably want to slip back
# to the terminal mode after setting options, but atm
# user.vim_normal_mode_exterm() implies no preservation
(show|set) highlight [search]: user.vim_normal_mode_exterm(":set hls\n")
(unset|set no|hide) highlight [search]: user.vim_normal_mode_exterm(":set nohls\n")
(show|set) line numbers: user.vim_normal_mode_exterm(":set nu\n")
(show|set) absolute line numbers:
    user.vim_normal_mode_exterm(":set norelativenumber\n")
    user.vim_normal_mode_exterm(":set number\n")
(show|set) relative line numbers:
    user.vim_normal_mode_exterm(":set nonumber\n")
    user.vim_normal_mode_exterm(":set relativenumber\n")
(unset|set no|hide) line numbers: user.vim_normal_mode_exterm(":set nonu\n")
show [current] settings: user.vim_normal_mode_exterm(":set\n")
(unset paste|set no paste): user.vim_normal_mode_exterm(":set nopaste\n")
# very useful for reviewing code you don't want to accidintally edit if talon
# mishears commands
set modifiable: user.vim_normal_mode_exterm(":set modifiable\n")
(unset modifiable|set no modifiable): user.vim_normal_mode_exterm(":set nomodifiable\n")

###
# Marks
###
new mark <user.letter>:
    user.vim_set_normal_mode_exterm()
    key(m)
    key(letter)
(go|jump) [to] mark <user.letter>:
    user.vim_set_normal_mode_exterm()
    key(`)
    key(letter)
(del|delete) (mark|marks):
    user.vim_normal_mode_exterm(":delmarks ")
(del|delete) all (mark|marks):
    user.vim_normal_mode_exterm(":delmarks! ")
(list|show) [all] marks:
    user.vim_normal_mode_exterm(":marks\n")
(list|show) specific marks:
    user.vim_normal_mode_exterm(":marks ")
(go|jump) [to] [last] edit: user.vim_normal_mode("`.")
(go|jump) [to] [last] (cursor|location): user.vim_normal_mode_exterm("``")

###
# Session
###
# XXX - to be made mode-aware
(make|save) session: user.vim_normal_mode_exterm(":mksession ")
force (make|save) session: user.vim_normal_mode_exterm(":mksession! ")
(load|open) session: user.vim_normal_mode_exterm(":source ")

###
# Macros and registers ''
###
show (registers|macros): user.vim_normal_mode(":reg\n")
show (register|macro) <user.letter>: user.vim_normal_mode(":reg {letter}\n")
play macro <user.letter>: user.vim_any_motion_mode("@{letter}")
repeat macro: "@@"
record macro <user.letter>: "q{letter}"
stop recording: key(q)
modify [register|macro] <user.letter>:
    ":let @{letter}='"
    key(ctrl-r)
    key(ctrl-r)
    insert("{letter}")
    key(')

# XXX - these could be valid in normal or visual
paste from register <user.any>: insert('"{any}p')
yank to register <user.any>: insert('"{any}y')

###
# Informational
###
display current line number: user.vim_normal_mode_key(ctrl-g)
file info: user.vim_normal_mode_key(ctrl-g)
# shows buffer number by pressing 2
extra file info:
    key(2)
    key(ctrl-g)
vim help: user.vim_normal_mode_exterm(":help ")

###
# Mode Switching
###
normal mode: user.vim_set_normal_mode_np()
insert mode: user.vim_set_insert_mode()
replace mode: key(R)
overwrite: key(R)

visual mode: user.vim_set_visual_mode()
(visual|select|highlight) line: key(V)

# XXX - need exterm
visual block mode: key(ctrl-v)
(visual|select|highlight) block: key(ctrl-v)

###
# Searching
###
# XXX - need exterm
search:
    user.vim_any_motion_mode("/\c")

search sensitive:
    key(escape)
    user.vim_any_motion_mode("/\C")

search <user.text>$:
    user.vim_any_motion_mode("/\c{text}\n")

search <user.text> sensitive$:
    user.vim_any_motion_mode("/\C{text}\n")

search <user.ordinals> <user.text>$:
    user.vim_any_motion_mode("{ordinals}/\c{text}\n")

search (reversed|reverse) <user.text>$:
    user.vim_any_motion_mode("?\c{text}\n")

search (reversed|reverse):
    user.vim_any_motion_mode("?\c")

search (reversed|reverse) sensitive:
    user.vim_any_motion_mode("?\C")

###
# Text Selection
###
select <user.vim_select_motion>:
    user.vim_visual_mode("{vim_select_motion}")

select lines <number> through <number>:
    user.vim_insert_mode_np("{number_1}G")
    user.vim_set_visual_mode()
    insert("{number_2}G")

###
# Convenience
###
run as python:
    user.vim_normal_mode_np(":w\n")
    insert(":exec '!python' shellescape(@%, 1)\n")

remove trailing white space: user.vim_normal_mode(":%s/\s\+$//e\n")
(remove all|normalize) tabs: user.vim_normal_mode(":%s/\t/    /eg\n")


###
# Auto completion
###
# XXX - revisit these you complete me plug in
complete: key(ctrl-n)
complete next: key(ctrl-n)
complete previous: key(ctrl-n)

###
# Visual Mode
###
(select|highlight) all: user.vim_normal_mode_np("ggVG")
reselect: user.vim_normal_mode_np("gv")

###
# Terminal mode
#
# NOTE: Only applicable to newer vim and neovim. Duplicate command with
# vim_terminal.talon, but included in case user doesn't have `VIM mode:t` in
# titlestring
###
(escape|pop) terminal:
    key(ctrl-\)
    key(ctrl-n)

# XXX - this may conflict with i3wm shell spawning
[new] (split|horizontal) (term|terminal):
    # NOTE: if your using zsh you might have to switch this, though depending
    # on your setup it will still work (this loads zsh on mine)
    user.vim_normal_mode_exterm(":split term://bash\n")

[new] vertical split (term|terminal):
    user.vim_normal_mode_exterm(":vsplit term://bash\n")

###
# Folding
###
fold (lines|line): user.vim_normal_mode("fZ")
fold line <number> through <number>$: user.vim_normal_mode(":{number_1},{number_2}fo\n")
(unfold|open fold|fold open): user.vim_normal_mode("zo")
(close fold|fold close): user.vim_normal_mode("zc")
open all folds: user.vim_normal_mode("zR")
close all folds: user.vim_normal_mode("zM")

###
# Plugins
###

# NOTE: These are here rather than nerdtree.talon to allow it to load the
# split buffer, which in turn loads nerdtree.talon when focused. Don't move
# these into nerdtree.talon for now
nerd tree: user.vim_normal_mode_exterm(":NERDTree\n")
nerd find [current] file: user.vim_normal_mode_exterm(":NERDTreeFind\n")

###
# Testing
###
# XXX - Just for testing random stuff. To be deleted
spider man:
    user.vim_normal_mode_keys("c")
