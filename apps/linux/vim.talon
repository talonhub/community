# Usage:
#  - See doc/vim.md
#  - See code/vim.py

os:linux
app:gvim
app:/term/
and win.title:/VIM/
-

tag(): vim

###
# Actions - Talon generic_editor.talon implementation
###
#
# NOTE: You can disable generic_editor.talon by renaming it, and still fully
# control vim. These are more for people that are used to the official talon
# editor commands that want to trial vim a bit.
#
# If you prefer to work from INSERT mode, you may want to add the ctrl-o key
# prior to most of these
#
# Note that I don't use any of the below, so they have not been thoroughly
# tested and the VISUAL mode selection stuff will almost certainly not work as
# expected.
###
action(edit.find):
    key(/)
action(edit.find_next):
    key(n)
action(edit.word_left):
    key(b)
action(edit.word_right):
    key(w)
action(edit.left):
    #key(ctrl-o)
    key(h)
action(edit.right):
    key(l)
action(edit.up):
    key(k)
action(edit.down):
    key(j)
action(edit.line_start):
    key(^)
action(edit.line_end):
    key($)
action(edit.file_end):
    key(G)
action(edit.file_start):
    "gg"
action(edit.page_down):
    key(ctrl-f)
action(edit.page_up):
    key(ctrl-b)
action(edit.extend_line_end):
    "v$"
action(edit.extend_left):
    "vh"
action(edit.extend_right):
    "vl"
action(edit.extend_line_up):
    "vk"
action(edit.extend_line_down):
    "vj"
action(edit.extend_word_left):
    "vb"
action(edit.extend_word_right):
    "vw"
action(edit.extend_line_start):
    "v^"
action(edit.extend_file_start):
    "vgg"
action(edit.extend_file_end):
    "vG"
action(edit.indent_more):
    ">>"
action(edit.indent_less):
    "<<"
action(edit.delete_line):
    "dd"
action(edit.delete):
    key(x)

# note these are for mouse highlighted copy/paste. shouldn't be used for actual
# vim commands
action(edit.copy):
    key(ctrl-shift-c)
action(edit.paste):
    key(ctrl-shift-v)

###
# `code/vim.py` actions based on vimspeak
###
<user.vim_normal_counted_command>:
    insert("{vim_normal_counted_command}")
<user.vim_motion_verbs_all>:
    insert("{vim_motion_verbs_all}")
<user.vim_normal_counted_action>:
    insert("{vim_normal_counted_action}")

###
# File editing and management
###
# NOTE: using `save` alone conflicts too much with the `say`
save file:
    key(escape)
    insert(":w\n")
save [file] as:
    key(escape)
    insert(":w ")
save all:
    key(escape)
    insert(":wa\n")
save and (quit|close):
    key(escape)
    insert(":wq\n")
(close|quit) file:
    key(escape)
    insert(":q\n")
force (close|quit):
    key(escape)
    insert(":q!\n")
refresh file:
    key(escape)
    insert(":e!\n")
edit [file|new]:
    insert(":e ")
reload [vim] config:
    insert(":so $MYVIMRC\n")

# For when the VIM cursor is hovering on a path
open [this] link: "gx"
open this file: "gf"
open this file in [split|window]:
    key(ctrl-w)
    key(f)
open this file in vertical [split|window]:
    insert(":vertical wincmd f\n")

list current directory: ":pwd\n"
change buffer directory: ":lcd %:p:h\n"

###
# Standard commands
###
redo:
    key(escape)
    key(ctrl-r)
undo:
    key(escape)
    key(u)

###
# Navigation, movement and jumping
#
# NOTE: Majority of more core movement verbs are in code/vim.py
###
[(go|jump)] [to] line <number>:
    key(escape)
    key(:)
    insert("{number}")
    key(enter)

matching: key(%)

# jump list
show jump list: ":jumps\n"
clear jump list: ":clearjumps\n"
(prev|previous|older) jump [entry]: key(ctrl-o)
(next|newer) jump [entry]: key(ctrl-i)

# ctags/symbol
(jump|dive) [to] (symbol|tag): key(ctrl-])
(pop|leave) (symbol|tag): key(ctrl-t)

# scrolling and page position
(focus|orient) [on] line <number>: ":{number}\nzt"
center [on] line <number>: ":{number}\nz."
scroll top: "zt"
scroll (center|middle): "zz"
scroll bottom: "zb"
scroll top reset cursor: "z\n"
scroll middle reset cursor: "z."
scroll bottom reset cursor: "z "
scroll up: key(ctrl-y)
scroll down: key(ctrl-e)
page down: key(ctrl-f)
page up: key(ctrl-b)
half [page] down: key(ctrl-d)
half [page] up: key(ctrl-u)

###
# Text editing, copying, and manipulation
###

change remaining line: key(C)
change line: "cc"
# XXX - this might be suited for some automatic motion thing in vim.py
swap characters: "xp"
swap words: "dwwP"
swap lines: "ddp"
swap paragraph: "d}}p"
replace <user.any>: "r{any}"
replace (ship|upper|upper case) <user.letters>:
    "r"
    user.keys_uppercase_letters(letters)

# indenting
(shift|indent) right: ">>"
indent [line] <number> through <number>$: ":{number_1},{number_2}>\n"
(shift|indent) left: "<<"
unindent [line] <number> through <number>$: ":{number_1},{number_2}>\n"


# XXX - this doesn't work with numbers below nine, because the nine will
# trigger its own discrete command in the first part of the command will
# trigger the dd below. we probably need to come up with different trigger for
# the one were you specify the line

# deleting
delete remaining line: key(D)
delete line (at|number) <number>$: ":{number}d\n"
delete line (at|number) <number> through <number>$: ":{number_1},{number_2}d\n"
delete line: "dd"

# insert mode only
clear line: key(ctrl-u)

# copying
(copy|yank) line (at|number) <number>$: ":{number}y\n"
(copy|yank) line (at|number) <number> through <number>: ":{number_1},{number_2}y\n"
(copy|yank) line: "Y"

# duplicating
(duplicate|paste) line <number> on line <number>$: ":{number_1}y\n:{number_2}\np"
(duplicate|paste) line (at|number) <number> through <number>$: ":{number_1},{number_2}y\np"
(duplicate|paste) line <number>$: ":{number}y\np"

(dup|duplicate) line: "Yp"

# start ending at end of line
push line:
    key(escape)
    key(A)

# start ending at end of file
push file:
    key(escape)
    insert("Go")

# helpful for fixing typos or bad lexicons that miss a character
inject <user.any> [before]:
    insert("i{any}")
    key(escape)

inject <user.any> after:
    insert("a{any}")
    key(escape)

filter line: "=="

[add] gap above: ":pu! _\n:'[+1\n"
[add] gap below: ":pu _\n:'[-1\n"

# XXX - This should be a callable function so we can do things like:
#       'swap on this <highlight motion>'
#       'swap between line x, y'
swap (selected|highlighted):
    insert(":")
    # leave time for vim to populate '<,'>
    sleep(50ms)
    insert("s///g")
    key(left)
    key(left)
    key(left)

# Selects current line in visual mode and triggers a word swap
swap [word] on [this] line:
    key(V)
    insert(":")
    sleep(50ms)
    insert("s///g")
    key(left)
    key(left)
    key(left)

deleted selected empty lines:
    insert(":")
    # leave time for vim to populate '<,'>
    sleep(50ms)
    insert("g/^$/d\j")

swap global:
    insert(":%s///g")
    key(left)
    key(left)
    key(left)

###
# Buffers
###
((buf|buffer) list|list (buf|buffer)s): ":ls\n"
(buf|buffer) (close|delete) <number>: ":bd {number} "
(close|delete) (buf|buffer) <number>: ":bd {number} "
(buf|buffer) close current: ":bd\n"
(delete|close) (current|this) buffer: ":bd\n"
force (buf|buffer) close: ":bd!\n"
(buf|buffer) open: ":b "
(buf|buffer) (first|rewind): ":br\n"
(buf|buffer) (left|prev): ":bprev\n"
(buf|buffer) (right|next): ":bnext\n"
# XXX - conflicts with actual :bl command.. maybe use flip?
(buf|buffer) last: ":b#\n"
close (bufs|buffers): ":bd "
[(go|jump|open)] (buf|buffer) <number>: ":b {number}\n"

###
# Splits
###
# creating splits
new split:
    key("ctrl-w")
    key(s)
new vertical split:
    key("ctrl-w")
    key(v)
split (close|quit):
    key(ctrl-w)
    key(q)

new empty split:
    key(escape)
    insert(":new\n")
new empty vertical split:
    key(escape)
    insert(":vnew\n")

# navigating splits
split <user.vim_arrow>:
    key(ctrl-w)
    key("{vim_arrow}")
split last:
    key(ctrl-w)
    key(p)
split top left:
    key(ctrl-w)
    key(t)
split next:
    key(ctrl-w)
    key(w)
split (previous|prev):
    key(ctrl-w)
    key(W)
split bottom right:
    key(ctrl-w)
    key(b)
split preview:
    key(ctrl-w)
    key(P)

# moving windows
split (only|exclusive):
    key(ctrl-w)
    key(o)
split rotate [right]:
    key(ctrl-w)
    key(r)
split rotate left:
    key(ctrl-w)
    key(R)
move split top:
    key(ctrl-w)
    key(K)
move split bottom:
    key(ctrl-w)
    key(J)
move split right:
    key(ctrl-w)
    key(H)
move split left:
    key(ctrl-w)
    key(L)
move split to tab:
    key(ctrl-w)
    key(T)

# window resizing
split (balance|equalize):
    key(ctrl-w)
    key(=)
split taller:
    key(ctrl-w)
    key(+)
split shorter:
    key(ctrl-w)
    key(-)
split fatter:
    key(ctrl-w)
    key(>)
split skinnier:
    key(ctrl-w)
    key(<)
set split width:
    key(escape)
    insert(":resize ")
set split height:
    key(escape)
    insert(":vertical resize ")

###
# Diffing
###
(split|window) start diff:
    key(escape)
    insert(":windo diffthis\n")

(split|window) end diff:
    key(escape)
    insert(":windo diffoff\n")

buffer start diff:
    key(escape)
    insert(":bufdo diffthis\n")

buffer end diff:
    key(escape)
    insert(":bufdo diffoff\n")

###
# Tabs
###
[show] tabs: ":tabs\n"
tab close: ":tabclose\n"
tab next: ":tabnext\n"
tab (prev|previous): ":tabprevious\n"
tab first: ":tabfirst\n"
tab last: ":tablast\n"

###
# Settings
###
(hide|unset) (highlight|hightlights): ":nohl\n"
set highlight search: ":set hls\n"
set no highlight search: ":set nohls\n"
(show|set) line numbers: ":set nu\n"
(hide|set no) line numbers: ":set nonu\n"
show [current] settings: ":set\n"
unset paste: ":set nopaste\n"
# very useful for reviewing code you don't want to accidintally edit if talon
# mishears commands
set modifiable: ":set modifiable\n"
unset modifiable: ":set nomodifiable\n"

###
# Marks
###
new mark <user.letter>:
    key(m)
    key(letter)
(go|jump) [to] mark <user.letter>:
    key(`)
    key(letter)
(del|delete) (mark|marks):
    key(escape)
    insert(":delmarks ")
(del|delete) all (mark|marks):
    key(escape)
    insert(":delmarks! ")
(list|show) [all] marks:
    key(escape)
    insert(":marks\n")
(list|show) specific marks:
    key(escape)
    insert(":marks ")
(go|jump) [to] [last] edit: "`."
(go|jump) [to] [last] (cursor|location): "``"

###
# Sessions
###
(make|save) session: ":mksession "
force (make|save) session: ":mksession! "

###
# Macros and registers
###
show registers: ":reg\n"
show register <user.letter>: ":reg {letter}\n"
play macro <user.letter>: "@{letter}"
repeat macro: "@@"
record macro <user.letter>: "q{letter}"
stop recording: key(q)
modify [register|macro] <user.letter>:
    ":let @{letter}='"
    key(ctrl-r)
    key(ctrl-r)
    insert("{letter}")
    key(')

paste from register <user.any>: '"{any}p'
yank to register <user.any>: '"{any}y'

###
# Informational
###
display current line number: key(ctrl-g)
file info: key(ctrl-g)
# shows buffer number by pressing 2
extra file info:
    key(2)
    key(ctrl-g)
vim help: ":help "

###
# Mode Switching
###
normal mode: key(escape)
insert mode: key(i)
replace mode: key(R)
overwrite: key(R)

visual mode: key(v)
(visual|select|highlight): key(v)
(visual|select|highlight) line: key(V)

visual block mode: key(ctrl-v)
(visual|select|highlight) block: key(ctrl-v)

###
# Searching
###
search:
    key(escape)
    insert("/\c")

search sensitive:
    key(escape)
    insert("/\C")

search <phrase>$:
    key(escape)
    insert("/\c{phrase}\n")

search <phrase> sensitive$:
    key(escape)
    insert("/\C{phrase}\n")

search <user.ordinals> <phrase>$:
    key(escape)
    insert("{ordinals}/\c{phrase}\n")

search (reversed|reverse) <phrase>$:
    key(escape)
    insert("?\c{phrase}\n")

search (reversed|reverse):
    key(escape)
    insert("?\c")

search (reversed|reverse) sensitive:
    key(escape)
    insert("?\C")

###
# Text Selection
###
select <user.vim_select_motion>:
    insert("v{vim_select_motion}")

select lines <number> through <number>:
    insert("{number_1}G")
    key(V)
    insert("{number_2}G")

###
# Convenience
###
run as python:
    insert(":w\n")
    insert(":exec '!python' shellescape(@%, 1)\n")

remove trailing white space: insert(":%s/\s\+$//e\n")
remove all tabs: insert(":%s/\t/    /eg\n")

# XXX - Just for testing run_vim_cmd. To be deleted
spider man:
    user.run_vim_cmd("beep")

###
# Auto completion
###
complete: key(ctrl-n)
complete next: key(ctrl-n)
complete previous: key(ctrl-n)

###
# Visual Mode
###
(visual|select|highlight) all: "ggVG"
reselect: "gv"

###
# Terminal mode
#
# NOTE: Only applicable to newer vim and neovim
###
(escape|pop) terminal:
    key(ctrl-\)
    key(ctrl-n)

###
# Folding
###
fold (lines|line): "fZ"
fold line <number> through <number>$: ":{number_1},{number_2}fo\n"
(unfold|open fold|fold open): "zo"
(close fold|fold close): "zc"
open all folds: "zR"
close all folds: "zM"

###
# Plugins
###

# NOTE: These are here rather than nerdtree.talon to allow it to load the
# split buffer, which in turn loads nerdtree.talon when focused. Don't move
# these into nerdtree.talon for now
nerd tree: insert(":NERDTree\n")
nerd find [current] file: insert(":NERDTreeFind\n")
