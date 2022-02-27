from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_comment_documentation", desc="Tag for enabling generic documentation commands")


@mod.action_class
class Actions:

    def code_comment_documentation():
        """Inserts a document comment and positions the cursor appropriately"""

    def code_comment_documentation_block():
        """Inserts a block document comment and positions the cursor appropriately"""

    def code_comment_documentation_inner():
        """Inserts an inner document comment and positions the cursor appropriately"""

    def code_comment_documentation_block_inner():
        """Inserts an inner block document comment and positions the cursor appropriately"""
