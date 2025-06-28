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

    def code_state_if():
        """Inserts if statement"""
        actions.user.insert_snippet_by_name("ifStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_if",
            'user.insert_snippet_by_name("ifStatement")',
        )

    def code_state_else_if():
        """Inserts else if statement"""
        actions.user.insert_snippet_by_name("elseIfStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_else_if",
            'user.insert_snippet_by_name("elseIfStatement")',
        )

    def code_state_else():
        """Inserts else statement"""
        actions.user.insert_snippet_by_name("elseStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_else",
            'user.insert_snippet_by_name("elseStatement")',
        )

    def code_state_do():
        """Inserts do statement"""
        actions.user.insert_snippet_by_name("doWhileLoopStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_do",
            'user.insert_snippet_by_name("doWhileLoopStatement")',
        )

    def code_state_switch():
        """Inserts switch statement"""
        actions.user.insert_snippet_by_name("switchStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_switch",
            'user.insert_snippet_by_name("switchStatement")',
        )

    def code_state_case():
        """Inserts case statement"""
        actions.user.insert_snippet_by_name("caseStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_case",
            'user.insert_snippet_by_name("caseStatement")',
        )

    def code_state_for():
        """Inserts for statement"""
        actions.user.insert_snippet_by_name("forLoopStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_for",
            'user.insert_snippet_by_name("forLoopStatement")',
        )

    def code_state_for_each():
        """Inserts for each equivalent statement"""
        actions.user.insert_snippet_by_name("forEachStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_for_each",
            'user.insert_snippet_by_name("forEachStatement")',
        )

    def code_state_go_to():
        """inserts go-to statement"""
        actions.user.insert_snippet_by_name("goToStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_go_to",
            'user.insert_snippet_by_name("goToStatement")',
        )

    def code_state_while():
        """Inserts while statement"""
        actions.user.insert_snippet_by_name("whileLoopStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_while",
            'user.insert_snippet_by_name("whileLoopStatement")',
        )

    def code_state_infinite_loop():
        """Inserts infinite loop statement"""
        actions.user.insert_snippet_by_name("infiniteLoopStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_infinite_loop",
            'user.insert_snippet_by_name("infiniteLoopStatement")',
        )

    def code_state_return():
        """Inserts return statement"""
        actions.user.insert_snippet_by_name("returnStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_state_return",
            'user.insert_snippet_by_name("returnStatement")',
        )

    def code_break():
        """Inserts break statement"""
        actions.user.insert_snippet_by_name("breakStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_break",
            'user.insert_snippet_by_name("breakStatement")',
        )

    def code_next():
        """Inserts next/continue statement"""
        actions.user.insert_snippet_by_name("continueStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_next",
            'user.insert_snippet_by_name("continueStatement")',
        )

    def code_try_catch():
        """Inserts try/catch. If selection is true, does so around the selection"""
        actions.user.insert_snippet_by_name("tryCatchStatement")
        actions.user.deprecate_action(
            "2025-06-24",
            "user.code_try_catch",
            'user.insert_snippet_by_name("tryCatchStatement")',
        )
