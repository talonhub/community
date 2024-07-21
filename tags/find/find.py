from talon import Module, Context, actions

mod = Module()
mod.tag("find", desc="Tag for enabling generic find commands")

ctx = Context()
ctx.matches = r"""
os: windows
os: linux
"""

ctx_mac = Context()
ctx_mac.matches = r"""
os: windows
"""


@ctx.action_class("edit")
class WinActions:
    def find(text: str = None):
        actions.key("ctrl-f")
        if text:
            actions.insert(text)


@ctx_mac.action_class("edit")
class MacActions:
    def find(text: str = None):
        actions.key("cmd-f")
        if text:
            actions.insert(text)
