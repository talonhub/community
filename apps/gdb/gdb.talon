os: linux
# XXX - this matches .gdb files atm
#win.title: /gdb/
tag: terminal
mode: user.gdb
-
tag(): user.gdb
tag(): user.debugger

##
# Generic debugger actions
##

# Code execution
action(user.debugger_step_into): "stepi\n"
action(user.debugger_step_over): "nexti\n"
action(user.debugger_step_line): "step\n"
action(user.debugger_step_over_line): "next\n"
action(user.debugger_step_out): "finish\n"
until <number>: "until {number}"
action(user.debugger_continue): "c\n"
action(user.debugger_stop): key("ctrl-c")
action(user.debugger_start): "run\n"
action(user.debugger_restart): "run\n"
# XXX -
action(user.debugger_detach): ""

# Registers
action(user.debugger_show_registers): "info registers\n"
action(user.debugger_get_register): "r "
action(user.debugger_set_register):
    insert("set $=")
    edit.left()

# Breakpoints
action(user.debugger_show_breakpoints): "info breakpoints\n"
action(user.debugger_add_sw_breakpoint): "break "
# XXX -
action(user.debugger_add_hw_breakpoint): ""
action(user.debugger_break_now): key("ctrl-c")
action(user.debugger_break_here): "break\n"
action(user.debugger_clear_all_breakpoints): "d br\n"
force clear all break points:
    insert("d br\n")
    insert("y\n")
action(user.debugger_clear_breakpoint):
    insert("d br ")
action(user.debugger_enable_all_breakpoints):
    insert("enable br\n")
action(user.debugger_enable_breakpoint):
    insert("enable br ")
action(user.debugger_disable_all_breakpoints):
    insert("disable br\n")
action(user.debugger_disable_breakpoint):
    insert("disable br  ")

break [on] clipboard:
    insert("break ")
    key(ctrl-shift-v)
    key(enter)

# Memory inspection

# Type inspection

##
# gdb specific functionality
##

# information
list [source]: "list\n"
info source: "info source\n"

print: "p "
print [variable] <user.text>: "p {text}"
print hex: "p/x "
print hex [variable] <user.text>: "p/x {text}"
print string: "p/s "

# hexdumping
# XXX - switch the sizes to a list in python?
# XXX - should cache the last used size
hex dump <number> bytes: "x/{number}bx "
hex dump <number> (half|short) words: "x/{number}hx "
hex dump <number> (d|long) words: "x/{number}dx "
hex dump <number> quad words: "x/{number}gx "
# this is some arbitrary default for convenience
hex dump: "x/100gx "
hex dump highlighted:
    insert("x/100gx ")
    edit.copy()
    edit.paste()
    key(enter)
hex dump clipboard:
    insert("x/100gx ")
    edit.paste()
    key(enter)


# execution
source: "source \t\t"

# displays
# XXX - move thee invoke command into a python script
(list|show|info) display: "info display\n"
display assembly line$: "display /i $pc\n"
display source: "display "
enable display <number_small>: "enable display {number_small}\n"
disable display <number_small>: "disable display {number_small}\n"
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
debug quit: "quit\n"
# more quickly quit when there are inferiors
debug force quit: "quit\ny\n"
(show|info) (inf|inferiors): "info inferiors\n"
inferior <number_small>$: "inferior {number_small}\n"
inferior: "inferior "
resume main (inf|inferior):
    insert("inferior 1\n")
    insert("c\n")
resume [from] (inf|inferior) <number_small>$:
    insert("inferior {number_small}\n")
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
set list size <number_small>: "set listsize {number_small}\n"

# misc
clear screen: "shell clear\n"
