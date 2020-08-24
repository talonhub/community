# XXX - trigger alt-1 to hit command window for necessary commands?
# ex: user.windbg_insert_in_cmd()
#    edit.left()

mode: user.windbg
-
tag(): user.debugger
tag(): user.windbg

##
# Generic debugger actions
##

# Code execution
action(user.debugger_step_into):
    key(f8)
action(user.debugger_step_over):
    key(f10)
# XXX -
action(user.debugger_step_line): ""
action(user.debugger_step_over_line): ""

action(user.debugger_step_out):
    key(shift-f11)
action(user.debugger_continue):
    key(f5)
action(user.debugger_stop):
    key(shift-f5)
action(user.debugger_restart):
    key(ctrl-shift-f5)
action(user.debugger_detach):
    insert(".detach")

# Registers
action(user.debugger_show_registers):
    key(r enter)
action(user.debugger_get_register):
    insert("r @")
action(user.debugger_set_register):
    insert("set $@=")
    edit.left()

# Breakpoints
action(user.debugger_show_breakpoints):
    insert("bl\n")
action(user.debugger_add_sw_breakpoint):
    insert("bp ")
action(user.debugger_add_hw_breakpoint):
    insert("ba e 1 ")
action(user.debugger_break_now):
    key(ctrl-break)
action(user.debugger_clear_all_breakpoints):
    insert("bc *\n")
action(user.debugger_clear_breakpoint):
    insert("bc ")
action(user.debugger_enable_all_breakpoints):
    insert("be *\n")
action(user.debugger_enable_breakpoint):
    insert("be ")
action(user.debugger_disable_all_breakpoints):
    insert("bd *\n")
action(user.debugger_disable_breakpoint):
    insert("bd ")

# Navigation
action(user.debugger_goto_address):
    insert("ctrl-g")
action(user.debugger_goto_clipboard):
    insert("ctrl-g")
    edit.paste()
    key(enter)
action(user.debugger_goto_highlighted):
    insert("ctrl-g")
    edit.copy()
    edit.paste()
    key(enter)


# Memory inspection
action(user.debugger_backtrace):
    key(k enter)
action(user.debugger_disassemble):
    key(u space)
action(user.debugger_disassemble_here):
    key(u enter)
action(user.debugger_disassemble_clipboard):
    key(u space)
    edit.paste()
    key(enter)
action(user.debugger_dump_ascii_string):
    insert("da ")
action(user.debugger_dump_unicode_string):
    insert("du ")
action(user.debugger_dump_pointers):
    insert("dps ")

action(user.debugger_list_modules):
    insert("lm\n")


# Registers XXX
register <user.registers>:
    key(@)
    insert("{registers}")

# Type inspection
action(user.debugger_inspect_type):
    insert("dt ")

# Convenience
action(user.debugger_clear_line):
    key("ctrl-a backspace")
##
# Windbg specific functionality
##

open help: insert(".hh\n")

# xxx - add window switching

add microsoft symbols:
    insert("srv*C:\symbols*http://msdl.microsoft.com/download/symbols;\n")
force reload symbols:
    insert(".reload /f\n")
reload symbols:
    insert(".reload\n")
loaded modules:
    insert("lm l\n")

display pointers:
    insert("dps ")

# XXX - should be generic
dereference pointer:
    insert("poi()")
    edit.left()

show version: key(ctrl-alt-w)

##
# Windows
##

view command: key(alt-1)
view watch: key(alt-2)
view locals: key(alt-3)
view registers: key(alt-4)
view memory: key(alt-5)
view call stack: key(alt-6)
view disassembly: key(alt-7)
view scratch pad: key(alt-8)
view (processes|threads): key(alt-9)

# XXX - temp
dump function params: "r @rcx,@rdx,@r8,@r9\n"

(lib|library) <user.windows_dlls>: "{windows_dlls}"
