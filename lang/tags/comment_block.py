from typing import Optional

from talon import Context, Module, actions

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
    def code_comment_block(text: Optional[str] = None):
        """Block comment"""
        actions.user.insert_snippet_by_name("commentBlock")
        if text is not None:
            actions.insert(text)

    def code_comment_block_prefix():
        """Block comment start syntax"""

    def code_comment_block_suffix():
        """Block comment end syntax"""

    def code_block_comment_line(text: Optional[str] = None):
        """Wraps current line in block comment markers. Puts `text` between them if given"""
        actions.edit.line_start()
        actions.user.code_comment_block_prefix()
        actions.key("space")
        if text is not None:
            actions.insert(text)
        actions.edit.line_end()
        actions.key("space")
        actions.user.code_comment_block_suffix()

    def code_start_line_with_block_comment(text: str):
        """Inserts a block comment at the start of the line"""
        actions.edit.line_start()
        actions.user.code_inline_block_comment(text)

    def code_end_line_with_block_comment(text: str):
        """Inserts a block comment at the end of the line"""
        actions.edit.line_end()
        actions.user.code_inline_block_comment(text)

    def code_inline_block_comment(text: str):
        """Inserts an inline block comment at the end of the line with the specified text"""
        actions.user.code_comment_block_prefix()
        actions.key("space")
        actions.insert(text)
        actions.key("space")
        actions.user.code_comment_block_suffix()


@c_like_ctx.action_class("user")
class CActions:
    def code_comment_block(text: Optional[str] = None):
        actions.insert("/*\n\n*/")
        actions.edit.up()
        if text is not None:
            actions.insert(text)

    def code_comment_block_prefix():
        actions.insert("/*")

    def code_comment_block_suffix():
        actions.insert("*/")
