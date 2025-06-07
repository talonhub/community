from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.tag(
    "code_comment_documentation", desc="Tag for enabling generic documentation commands"
)


@mod.action_class
class Actions:
    def code_comment_documentation():
        """Inserts a document comment and positions the cursor appropriately"""
        actions.user.insert_snippet_by_name("commentDocumentation")
