from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag(
    "code_imperative",
    desc="Tag for enabling basic imperative programming commands (loops, functions, etc)",
)


@mod.action_class
class Actions:
    def code_block():
        """Inserts equivalent of {\n} for the active language, and places the cursor appropriately"""

    def code_state_if():
        """Inserts if statement"""

    def code_state_else_if():
        """Inserts else if statement"""

    def code_state_else():
        """Inserts else statement"""

    def code_state_do():
        """Inserts do statement"""

    def code_state_switch():
        """Inserts switch statement"""

    def code_state_case():
        """Inserts case statement"""

    def code_state_for():
        """Inserts for statement"""

    def code_state_for_each():
        """Inserts for each equivalent statement"""

    def code_state_go_to():
        """inserts go-to statement"""

    def code_state_while():
        """Inserts while statement"""

    def code_state_infinite_loop():
        """Inserts infinite loop statement"""

    def code_state_return():
        """Inserts return statement"""

    def code_break():
        """Inserts break statement"""

    def code_next():
        """Inserts next statement"""

    def code_try_catch():
        """Inserts try/catch. If selection is true, does so around the selection"""
