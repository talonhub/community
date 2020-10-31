from talon import Context, Module, actions, ui

mod = Module()
ctx = Context()

ctx.matches = r"""
mode: user.windbg
"""

ctx.lists["self.windows_dlls"] = {
    "core": "ntdll",
    "en tea": "ntdll",
    "user": "user32",
}


@mod.capture(rule="{self.windows_dlls}")
def windows_dlls(m) -> str:
    "Return an register"
    return m.windows_dlls


@ctx.action_class("user")
class user_actions:
    def debugger_clear_breakpoint_id(number_small: int):
        actions.insert(f"bc {number_small}\n")

    def debugger_disable_breakpoint_id(number_small: int):
        actions.insert(f"bd {number_small}\n")

    def debugger_enable_breakpoint_id(number_small: int):
        actions.insert(f"be {number_small}\n")
