from talon import Context, Module, actions
from typing import Optional

c_like_ctx = Context()
mod = Module()

mod.tag("code_comment_block", desc="Tag for enabling generic block comment commands")
mod.tag("code_comment_block_c_like", desc="Denotes usage of C-style block comments")

c_like_ctx.matches = """
tag: user.code_comment_block_c_like
"""
c_like_ctx.tags = ["user.code_comment_block"]


@mod.action_class
class Actions:
    def code_comment_block():
        """Block comment"""
        actions.user.insert_snippet_by_name("commentBlock")

    def code_comment_block_prefix():
        """Block comment start syntax"""

    def code_comment_block_suffix():
        """Block comment end syntax"""

    def code_block_comment_line(text: Optional[str]=None):
        """Block comment line"""
        actions.edit.line_start()
        actions.user.code_comment_block_prefix()
        actions.key("space")
        if text is not None:
            actions.insert(text)
        actions.edit.line_end()
        actions.key("space")
        actions.user.code_comment_block_suffix()

@c_like_ctx.action_class("user")
class CActions:
    def code_comment_block():
        actions.insert("/*\n\n*/")
        actions.edit.up()

    def code_comment_block_prefix():
        actions.insert("/*")

    def code_comment_block_suffix():
        actions.insert("*/")
