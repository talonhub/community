from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.tag("code_comment_block", desc="Tag for enabling generic block comment commands")
mod.tag("code_comment_block_c_like", desc="Denotes usage of C-style block comments")

ctx.matches = """
tag: user.code_comment_block_c_like
"""
ctx.tags = ["user.code_comment_block"]


@mod.action_class
class Actions:
    def code_comment_block():
        """Block comment"""

    def code_comment_block_prefix():
        """Block comment start syntax"""

    def code_comment_block_suffix():
        """Block comment end syntax"""


@ctx.action_class("user")
class CActions:
    def code_comment_block():
        actions.insert("/*\n\n*/")
        actions.edit.up()

    def code_comment_block_prefix():
        actions.auto_insert("/*")

    def code_comment_block_suffix():
        actions.auto_insert("*/")
