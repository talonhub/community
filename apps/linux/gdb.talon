os: linux
app: /term/
# XXX - this matches .gdb files atm
win.title: /gdb/
-

# information
list [source]: "list\n"
info source: "info source\n"

print: "p "
print [variable] <phrase>: "p {phrase}"
print hex: "p/x "
print hex [variable] <phrase>: "p/x {phrase}"

### Breakpoints ###

# enable
(list|show|info) breakpoints: "info breakpoints\n"
break [point] [on]: "break "
break [point] here: "break\n"
enable all break points: "enable br\n"
enable break [point] <number>: "enable br {number}\n"
break [on] clipboard: 
    insert("break ")
    key(ctrl-shift-v)
    key(enter)

# disable
disable all break points: "disable br\n"
disable break [point] <number>: "disable br {number}\n"

# delete
delete all break points: "d br\n"
force delete all break points: 
    insert("d br\n")
    insert("y\n")
delete break [point] <number>: "d br {number}"

until <number>: "until {number}"
finish [function]: "finish\n"

# registers
(list|show|info) registers: "info registers\n"

# execution
(rerun|run): "run\n"
source: "source \t\t"

# stepping
step [into]: "step\n"
(step over|next) [line]: "next\n"

# displays
# XXX - move thee invoke command into a python script
(list|show|info) display: "info display\n"
display assembly line$: "display /i $pc\n"
display source: "display "
enable display <number>: "enable display {number}\n"
disable display <number>: "disable display {number}\n"
undisplay: "undisplay\n"

# variables
(list|show|info) local: "info local "
(list|show|info) local typed: "info local -t "
(list|show|info) variable: "info variable "
(list|show|info) variable typed: "info variable -t "
(list|show|info) locals: "info local\n"
(list|show|info) variables: "info variables\n"

# threads
info threads: "info threads\n"

restart [program]: "r\n"
continue: "c\n"
back trace: "bt\n"
quit: "quit\n"
# more quickly quit when there are inferiors 
force quit: "quit\ny\n"
(show|info) (inf|inferiors): "info inferiors\n"
inferior <number>$: "inferior {number}\n"
inferior: "inferior "
resume main (inf|inferior):
    insert("inferior 1\n")
    insert("c\n")
resume [from] (inf|inferior) <number>$: 
    insert("inferior {number}\n")
    insert("c\n")

# arguments
set args: "set args "

# settings
show follow (fork|forks) [mode]: "show follow-fork-mode\n"
[set] follow (fork|forks) [mode] child: "set follow-fork-mode child\n"
[set] follow (fork|forks) [mode] parent: "set follow-fork-mode parent\n"

show detach on fork: "show detach-on-fork\n"
set detach on fork: "set detach-on-fork on\n"
unset detach on fork: "set detach-on-fork off\n"

# list
show list size: "show listsize\n"
set list size <number>: "set listsize {number}\n"

# misc
clear screen: "shell clear\n"

