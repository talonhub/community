from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_data_null", desc="Tag for enabling commands relating to null")


@mod.action_class
class Actions:
    def code_insert_null():
        """Inserts null"""

    def code_insert_is_null():
        """Inserts check for null"""

    def code_insert_is_not_null():
        """Inserts check for non-null"""
