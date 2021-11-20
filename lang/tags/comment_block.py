from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_comment_block", desc="Tag for enabling generic block comment commands")

@mod.action_class
class Actions:

    def code_comment_block():
        """Block comment"""

    def code_comment_block_prefix():
        """Block comment start syntax"""

    def code_comment_block_suffix():
        """Block comment end syntax"""
