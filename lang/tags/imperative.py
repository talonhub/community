from talon import Context, Module, actions

c_like_ctx = Context()
mod = Module()

mod.tag(
    "code_imperative",
    desc="Tag for enabling basic imperative programming commands (loops, functions, etc)",
)
mod.tag("code_block_c_like", desc="Language uses C style code blocks, i.e. braces")

c_like_ctx.matches = """
tag: user.code_block_c_like
"""


@mod.action_class
class Actions:
    def code_block():
        """Inserts equivalent of {\n} for the active language, and places the cursor appropriately"""

    def code_state_if():
        """Inserts if statement"""
        actions.user.insert_snippet_by_name("ifStatement")

    def code_state_else_if():
        """Inserts else if statement"""
        actions.user.insert_snippet_by_name("elseIfStatement")

    def code_state_else():
        """Inserts else statement"""
        actions.user.insert_snippet_by_name("elseStatement")

    def code_state_do():
        """Inserts do statement"""
        actions.user.insert_snippet_by_name("doWhileLoopStatement")

    def code_state_switch():
        """Inserts switch statement"""
        actions.user.insert_snippet_by_name("switchStatement")

    def code_state_case():
        """Inserts case statement"""
        actions.user.insert_snippet_by_name("caseStatement")

    def code_state_for():
        """Inserts for statement"""
        actions.user.insert_snippet_by_name("forLoopStatement")

    def code_state_for_each():
        """Inserts for each equivalent statement"""
        actions.user.insert_snippet_by_name("forEachStatement")

    def code_state_go_to():
        """inserts go-to statement"""
        actions.user.insert_snippet_by_name("goToStatement")

    def code_state_while():
        """Inserts while statement"""
        actions.user.insert_snippet_by_name("whileLoopStatement")

    def code_state_infinite_loop():
        """Inserts infinite loop statement"""
        actions.user.insert_snippet_by_name("infiniteLoopStatement")

    def code_state_return():
        """Inserts return statement"""
        actions.user.insert_snippet_by_name("returnStatement")

    def code_break():
        """Inserts break statement"""
        actions.user.insert_snippet_by_name("breakStatement")

    def code_next():
        """Inserts next/continue statement"""
        actions.user.insert_snippet_by_name("continueStatement")

    def code_try_catch():
        """Inserts try/catch. If selection is true, does so around the selection"""
        actions.user.insert_snippet_by_name("tryCatchStatement")


@c_like_ctx.action_class("user")
class CActions:
    def code_block():
        actions.user.insert_between("{", "}")
        actions.key("enter")
