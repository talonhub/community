from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_block_comment", desc="Tag for enabling generic block comment commands")

@mod.action_class
class Actions:

    def code_block_comment():
        """Block comment"""

    def code_block_comment_prefix():
        """Block comment start syntax"""

    def code_block_comment_suffix():
        """Block comment end syntax"""
