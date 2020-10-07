from talon import Context, Module, actions, ui

ctx = Context()

ctx.matches = r"""
mode: user.gdb
"""


@ctx.action_class("user")
class user_actions:
    def debugger_clear_breakpoint_id(number_small: int):
        actions.insert(f"d br {number_small}\n")

    def debugger_disable_breakpoint_id(number_small: int):
        actions.insert(f"disable br {number_small}\n")

    def debugger_enable_breakpoint_id(number_small: int):
        actions.insert(f"enable br {number_small}\n")
