from talon import Context, Module, actions

mod = Module()

mod.tag(
    "code_imperative",
    desc="Tag for enabling basic imperative programming commands (loops, functions, etc)",
)


@mod.action_class
class Actions:
    def code_block():
        """Inserts equivalent of {\n} for the active language, and places the cursor appropriately"""
        actions.user.insert_snippet_by_name("codeBlock")
