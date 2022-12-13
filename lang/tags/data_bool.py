from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_data_bool", desc="Tag for enabling commands for inserting Boolean data")

@mod.action_class
class Actions:

    def code_insert_true():
        """Insert True value"""

    def code_insert_false():
        """Insert False value"""
