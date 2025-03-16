from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_data_null", desc="Tag for enabling commands relating to null")
mod.list("code_data_null", desc="null-like value (e.g. Python `None`, C++ `nullptr`)")

ctx.lists["self.code_data_null"] = {
    "null": "null",
    # backwards compatibility
    "nil": "null",
    "none": "null",
}


@mod.action_class
class Actions:
    def code_insert_is_null():
        """Inserts check for null"""

    def code_insert_is_not_null():
        """Inserts check for non-null"""
