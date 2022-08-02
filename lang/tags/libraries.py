from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag(
    "code_libraries",
    desc="Tag for enabling commands for importing libraries",
)


@mod.action_class
class Actions:
    def code_import():
        """import/using equivalent"""
