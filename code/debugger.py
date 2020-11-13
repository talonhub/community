# XXX - execute until line number/cursor
# XXX - more memory printing he thumping

from talon import Context, Module

mod = Module()
mod.tag("debugger", desc="Tag for enabling generic debugger commands")

ctx = Context()
ctx.matches = r"""
tag: debugger
"""

x86_registers = {
    "air": "eax",
    "bat": "ebx",
    "cap": "ecx",
    "drum": "edx",
    "source": "esi",
    "dest": "edi",
    "stack": "esp",
    "frame": "ebp",
    "instruction": "eip",
}

x64_registers = {
    # general purpose
    "air": "rax",
    "racks": "rax",
    "bat": "rbx",
    "cap": "rcx",
    "drum": "rdx",
    "source": "rsi",
    "dest": "rdi",
    "stack": "rsp",
    "stack pointer": "rsp",
    "frame": "rbp",
    "frame pointer": "rbp",
    "base": "rbp",
    "base pointer": "rbp",
    "eight": "r8",
    "nine": "r9",
    "ten": "r10",
    "eleven": "r11",
    "twelve": "r12",
    "thirteen": "r13",
    "fourteen": "r14",
    "fifteen": "r15",
    # pointers
    "instruction": "rip",
    "rip": "rip",
    # segment
}

# XXX - pass by windbg to dump
windows_x64_register_parameters = ["rcx", "rdx", "r8", "r9"]

# XXX - make this dynamic
ctx.lists["self.registers"] = x64_registers

# assembly_languages = {
#    "x86": x86_registers,
#    "x64": x64_registers,
# }

mod.list("registers", desc="Main architecture register set")


@mod.capture(rule="{self.registers}")
def registers(m) -> str:
    "Returns a register"
    return m.registers


@mod.action_class
class Actions:
    def debugger_step_into():
        """Step into an instruction in the debugger"""

    def debugger_step_over():
        """Step over an instruction in the debugger"""

    def debugger_step_line():
        """Step into a source line in the debugger"""

    def debugger_step_over_line():
        """Step over a source line in the debugger"""

    def debugger_step_out():
        """Step until function exit in the debugger"""

    def debugger_continue():
        """Continue execution in the debugger"""

    def debugger_restart():
        """Restart execution in the debugger"""

    def debugger_start():
        """Start debugging"""

    def debugger_stop():
        """Stop the debugger"""

    def debugger_exit():
        """Exit the debugger"""

    def debugger_detach():
        """Detach the debugger"""

    def debugger_backtrace():
        """Print a back trace in the debugger"""

    def debugger_get_register():
        """Print specific register in the debugger"""

    def debugger_set_register():
        """Set specific register in the debugger"""

    def debugger_show_registers():
        """Print the current registers in the debugger"""

    def debugger_break_now():
        """Break into the debugger"""

    def debugger_break_here():
        """Set a break on the current line"""

    def debugger_show_breakpoints():
        """Print the current breakpoints in the debugger"""

    def debugger_add_sw_breakpoint():
        """Add one software breakpoint in the debugger"""

    def debugger_add_hw_breakpoint():
        """Add one hardware breakpoint in the debugger"""

    def debugger_clear_all_breakpoints():
        """Clear all breakpoints in the debugger"""

    def debugger_clear_breakpoint():
        """Clear one breakpoint in the debugger"""

    def debugger_clear_breakpoint_id(number_small: int):
        """Clear one breakpoint id in the debugger"""

    def debugger_disable_breakpoint_id(number_small: int):
        """Disable one breakpoint id in the debugger"""

    def debugger_disable_breakpoint():
        """Disable one breakpoint in the debugger"""

    def debugger_disable_all_breakpoints():
        """Disable all breakpoints in the debugger"""

    def debugger_enable_breakpoint():
        """Enable one breakpoint in the debugger"""

    def debugger_enable_breakpoint_id(number_small: int):
        """Enable one breakpoint id in the debugger"""

    def debugger_enable_all_breakpoints():
        """Enable all breakpoints in the debugger"""

    def debugger_disassemble():
        """Preps the disassemble command in the debugger"""

    def debugger_disassemble_here():
        """Disassembles instructions at the current instruction pointer"""

    def debugger_disassemble_clipboard():
        """Disassemble instructions at an address in the clipboard"""

    def debugger_goto_address():
        """Jump to a specific address in the debugger"""

    def debugger_goto_clipboard():
        """Jump to a specific address stored in the clipboard"""

    def debugger_goto_highlighted():
        """Jump to a specific highlighted address in the debugger"""

    def debugger_dump_ascii_string():
        """Display as specific address as an ascii string in the debugger"""

    def debugger_dump_unicode_string():
        """Display as specific address as an unicode string in the debugger"""

    def debugger_dump_pointers():
        """Display as specific address as a list of pointers in the debugger"""

    def debugger_inspect_type():
        """Inspect a specific data type in the debugger"""

    def debugger_clear_line():
        """Clear unwanted data from the command line"""

    def debugger_list_modules():
        """List the loaded modules in the debuggee memory space"""
