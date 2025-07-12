from talon import Context, Module, actions

from ..tags.operators import Operators

ctx = Context()
ctx.matches = r"""
code.language: sql
"""

mod = Module()
mod.list("sql_select", desc="Beginning of a select statement")
mod.list("sql_join", desc="Beginning of a join statement")

@mod.action_class
class Actions:
    def sql_alias(text: str):
        """Creates an alias from a string"""
        chars = [w[0] for w in str(text).split(" ")]
        return "".join(chars)
    
    def sql_insert(text: str):
        """Insert, adding a space if needed"""
        before, _ = actions.user.dictation_peek(True, False)
        if before and before[-1] != " " and before[-1] != "\n":
            actions.insert(" ")
        actions.insert(text)

@mod.capture(rule="(<user.sql_table> | <user.letters>)")
def sql_alias(m) -> str:
    return actions.user.sql_alias(m)

@mod.capture(rule="<user.text>")
def sql_table(m) -> str:
    return actions.user.formatted_text(m, "SNAKE_CASE")

@mod.capture(rule="<user.sql_table> [as <user.sql_alias>]")
def sql_table_with_alias(m) -> str:
    alias = getattr(m, "sql_alias", actions.user.sql_alias(m.sql_table))
    return f"{m.sql_table} {alias}"

@mod.capture(rule="<user.text>")
def sql_column(m) -> str:
    return actions.user.formatted_text(m, "SNAKE_CASE")

@mod.capture(rule="[<user.sql_alias> dot] <user.sql_column>")
def sql_field(m) -> str:
    return str(m).replace(" dot ", ".").strip()

@mod.capture(rule="on <user.sql_field> [equals <user.sql_field>]")
def sql_field_equals(m) -> str:
    return m.replace(" equals ", " = ")

operators = Operators(
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_EQUAL=" = ",
    MATH_NOT_EQUAL=" <> ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_IN=lambda: actions.user.insert_between(" IN (", ")"),
    MATH_NOT_IN=lambda: actions.user.insert_between(" NOT IN (", ")"),
    MATH_AND=" AND ",
    MATH_OR=" OR ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_insert_null():
        actions.auto_insert("NULL")

    def code_insert_is_null():
        actions.auto_insert(" IS NULL")

    def code_insert_is_not_null():
        actions.auto_insert(" IS NOT NULL")

    def code_insert_function(text: str, selection: str):
        substitutions = {"1": text}
        if selection:
            substitutions["0"] = selection
        actions.user.insert_snippet_by_name("functionCall", substitutions)
