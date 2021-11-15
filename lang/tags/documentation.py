from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_documentation", desc="Tag for enabling generic documentation commands")

@mod.action_class
class Actions:

    def code_document_string():
        """Inserts a document string and positions the cursor appropriately"""
