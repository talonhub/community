from talon import Context, Module, actions

mod = Module()
mod.tag("gdb", "Tag to enabled gdb-related functionality")

# user.gdb-specific context
ctx_gdb_enabled = Context()
ctx_gdb_enabled.matches = r"""
tag: user.gdb
"""

# global context for enabling and disabling user.gdb tag
ctx_global = Context()


@mod.action_class
class Actions:
    def gdb_enable():
        """Enables the gdb tag"""
        ctx_global.tags = ["user.gdb"]

    def gdb_disable():
        """Disables the gdb tag"""
        ctx_global.tags = []


@ctx_gdb_enabled.action_class("user")
class UserActions:
    ##
    # Generic debugger actions
    ##

    # Code execution
    def debugger_step_into():
        actions.auto_insert("stepi\n")

    def debugger_step_over():
        actions.auto_insert("nexti\n")

    def debugger_step_line():
        actions.auto_insert("step\n")

    def debugger_step_over_line():
        actions.auto_insert("next\n")

    def debugger_step_out():
        actions.auto_insert("finish\n")

    def debugger_continue():
        actions.auto_insert("c\n")

    def debugger_stop():
        actions.key("ctrl-c")

    def debugger_start():
        actions.auto_insert("run\n")

    def debugger_restart():
        actions.auto_insert("run\n")

    # XXX -
    def debugger_detach():
        actions.auto_insert("")

    # Registers
    def debugger_show_registers():
        actions.auto_insert("info registers\n")

    def debugger_get_register():
        actions.auto_insert("r ")

    def debugger_set_register():
        actions.user.insert_between("set $", "=")
        # Breakpoints

    def debugger_show_breakpoints():
        actions.auto_insert("info breakpoints\n")

    def debugger_add_sw_breakpoint():
        actions.auto_insert("break ")

    # XXX -
    def debugger_add_hw_breakpoint():
        actions.auto_insert("")

    def debugger_break_now():
        actions.key("ctrl-c")

    def debugger_break_here():
        actions.auto_insert("break\n")

    def debugger_clear_all_breakpoints():
        actions.auto_insert("d br\n")

    def debugger_clear_breakpoint():
        actions.insert("d br ")

    def debugger_enable_all_breakpoints():
        actions.insert("enable br\n")

    def debugger_enable_breakpoint():
        actions.insert("enable br ")

    def debugger_disable_all_breakpoints():
        actions.insert("disable br\n")

    def debugger_disable_breakpoint():
        actions.insert("disable br  ")

    def debugger_clear_breakpoint_id(number_small: int):
        actions.insert(f"d br {number_small}\n")

    def debugger_disable_breakpoint_id(number_small: int):
        actions.insert(f"disable br {number_small}\n")

    def debugger_enable_breakpoint_id(number_small: int):
        actions.insert(f"enable br {number_small}\n")
