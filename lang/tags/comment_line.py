from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_comment_line", desc="Tag for enabling generic line comment commands")

@mod.action_class
class Actions:

    def code_comment_line():
        """Inserts comment at current cursor location"""
