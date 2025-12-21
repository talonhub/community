from talon import Context, Module, actions

mod = Module()

mod.tag("code_comment_block", desc="Tag for enabling generic block comment commands")
mod.tag("code_comment_block_c_like", desc="Denotes usage of C-style block comments")

@mod.action_class
class Actions:
    def code_comment_block():
        """Block comment"""
        actions.user.insert_snippet_by_name("commentBlock")

    def code_comment_block_prefix():
        """Block comment start syntax"""

    def code_comment_block_suffix():
        """Block comment end syntax"""
