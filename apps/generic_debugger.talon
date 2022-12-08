tag: debugger
-

# Code execution

## instruction level
step into: user.debugger_step_into()
step over: user.debugger_step_over()

## line level
step line: user.debugger_step_line()
step over line: user.debugger_step_over_line()
step out: user.debugger_step_out()
continue: user.debugger_continue()

## these are multi word to avoid accidental utterance
debug start: user.debugger_start()
debug stop: user.debugger_stop()
debug exit: user.debugger_exit()
debug detach: user.debugger_detach()
debug restart: user.debugger_restart()

# Register
show registers: user.debugger_show_registers()
# XXX -
get register: user.debugger_get_register()
set register: user.debugger_set_register()

# Breakpoints
break now: user.debugger_break_now()
break here: user.debugger_break_here()
(list | show) (breaks | break points): user.debugger_show_breakpoints()
(set | add) (break | break point): user.debugger_add_sw_breakpoint()
(set | add) hardware (break | break point): user.debugger_add_hw_breakpoint()
clear all (breaks | break points): user.debugger_clear_all_breakpoints()
clear (break | break point): user.debugger_clear_breakpoint()
clear (break | break point) <number_small>:
    user.debugger_clear_breakpoint_id(number_small)
disable all (breaks | break points): user.debugger_disable_all_breakpoints()
disable (break | break point): user.debugger_disable_breakpoint()
disable (break | break point) <number_small>:
    user.debugger_disable_breakpoint_id(number_small)
enable all (breaks | break points): user.debugger_enable_all_breakpoints()
enable (break | break point): user.debugger_enable_breakpoint()
enable (break | break point) <number_small>:
    user.debugger_enable_breakpoint_id(number_small)

# Navigation

# Memory Inspection
(stack | back) trace: user.debugger_backtrace()
disassemble: user.debugger_disassemble()
disassemble here: user.debugger_disassemble_here()
disassemble clipboard: user.debugger_disassemble_clipboard()
jump to address: user.debugger_goto_address()
jump to clipboard: user.debugger_goto_clipboard()
jump to highlighted: user.debugger_goto_highlighted()

dump string: user.debugger_dump_ascii_string()
dump unicode [string]: user.debugger_dump_unicode_string()
dump pointers: user.debugger_dump_pointers()

list modules: user.debugger_list_modules()

# Type inspection
inspect type: user.debugger_inspect_type()

# Hex Dumping Memory
#hex dump register:

# Convenience
clear line: user.debugger_clear_line()
