from talon import Context, Module, actions, settings

from ..tags.operators import Operators
ctx = Context()
mod = Module()
ctx.matches = r"""
code.language: elixir
"""

# Elixir keywords and constructs
ctx.lists["user.code_keyword"] = {
    "def": "def ",
    "def p": "defp ",
    "def module": "defmodule ",
    "do": "do ",
    "end": "end",
    "if": "if ",
    "else": "else ",
    "cond": "cond ",
    "case": "case ",
    "when": "when ",
    "f n": "fn ",
    "receive": "receive ",
    "after": "after ",
    "try": "try ",
    "catch": "catch ",
    "rescue": "rescue ",
    "raise": "raise ",
    "with": "with ",
    "unless": "unless ",
    "import": "import ",
    "alias": "alias ",
    "require": "require ",
    "use": "use ",
}

operators = Operators(
    LAMBDA="->",

    ASSIGNMENT=" = ",

    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" and ",
    MATH_OR=" or ",
)

@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_comment_line_prefix():
        actions.insert("# ")

    def code_self():
        actions.auto_insert("self")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_insert_null():
        actions.insert("nil")

    def code_insert_is_null():
        actions.insert(" == nil")

    def code_insert_is_not_null():
        actions.insert(" != nil")

    def code_state_if():
        actions.user.insert_between("if ", " do\nend")

    def code_state_else_if():
        actions.user.insert_between("else if ", " do\nend")

    def code_state_else():
        actions.insert("else\nend")
        actions.key("enter")

    def code_state_case():
        actions.user.insert_between("case ", " do\nend")

    def code_state_for():
        actions.user.insert_between("for ", " do\nend")

    def code_state_while():
        actions.user.insert_between("while ", " do\nend")

    def code_define_class():
        # Elixir doesn't have classes, so this is not applicable
        pass

    def code_state_return():
        # Elixir functions automatically return the last evaluated expression
        pass

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_default_function(text: str):
        result = "def {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )
        actions.user.code_insert_function(result, None)

    def code_public_function(text: str):
        actions.user.code_default_function(text)

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "defp {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )
        actions.user.code_insert_function(result, None)

    def code_import_module(text: str):
        actions.auto_insert("import ")
        actions.insert(text)

    def code_alias_module(text: str):
        actions.auto_insert("alias ")
        actions.insert(text)

    def code_require_module(text: str):
        actions.auto_insert("require ")
        actions.insert(text)

    def code_use_module(text: str):
        actions.auto_insert("use ")
        actions.insert(text)
