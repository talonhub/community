from talon import Context, Module, actions

mod = Module()
mod.tag("find", desc="Tag for enabling generic find commands")

ctx = Context()

ctx_mac = Context()
ctx_mac.matches = r"""
os: mac
"""


@ctx.action_class("edit")
class EditActions:
    def find(text: str = None):
        actions.key("ctrl-f")
        if text:
            actions.insert(text)


@ctx_mac.action_class("edit")
class MacEditActions:
    def find(text: str = None):
        actions.key("cmd-f")
        if text:
            actions.insert(text)
