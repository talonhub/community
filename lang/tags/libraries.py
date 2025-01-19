from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag(
    "code_libraries",
    desc="Tag for enabling commands for importing libraries",
)

mod.list("code_libraries", desc="List of libraries for active language")


@mod.capture(rule="{user.code_libraries}")
def code_libraries(m) -> str:
    """Returns a type"""
    return m.code_libraries


@mod.action_class
class Actions:
    def code_import():
        """import/using equivalent"""

    def code_insert_library(text: str, selection: str):
        """Inserts a library and positions the cursor appropriately"""
