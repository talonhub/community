from talon import Context, Module, actions, settings

mod = Module()
ctx = Context()
ctx.matches = r"""
mode: user.sql
mode: user.auto_lang
and code.language: sql
"""

ctx.lists["user.code_functions"] = {
    "distinct": "DISTINCT",
    "average": "AVG",
    "first": "FIRST",
    "last": "LAST",
    "max": "MAX",
    "min": "MIN",
    "sum": "SUM",
    "timestamp": "TIMESTAMP",
    "count": "COUNT",
    "cast": "CAST",
}

sql_join_types = [
    "LEFT",
    "RIGHT",
    "INNER",
    "OUTER"
]
mod.list("sql_join_types", desc="Types of JOIN in SQL")
ctx.lists["user.sql_join_types"] = sql_join_types

@ctx.action_class("user")
class UserActions:
    def code_operator_subtraction():                     actions.auto_insert(" - ")
    def code_operator_addition():                        actions.auto_insert(" + ")
    def code_operator_multiplication():                  actions.auto_insert(" * ")
    def code_operator_division():                        actions.auto_insert(" / ")
    def code_operator_modulo():                          actions.auto_insert(" % ")
    def code_operator_equal():                           actions.auto_insert(" = ")
    def code_operator_not_equal():                       actions.auto_insert(" != ")
    def code_operator_greater_than():                    actions.auto_insert(" > ")
    def code_operator_greater_than_or_equal_to():        actions.auto_insert(" >= ")
    def code_operator_less_than():                       actions.auto_insert(" < ")
    def code_operator_less_than_or_equal_to():           actions.auto_insert(" <= ")
    def code_null():                                     actions.auto_insert("NULL")
    def code_is_null():                                  actions.auto_insert(" IS NULL")
    def code_is_not_null():                              actions.auto_insert(" IS NOT NULL")
    def code_insert_function(text: str, selection: str):
            if selection:
                text = text + "({})".format(selection)
            else:
                text = text + "()"
            actions.insert(text)
            actions.edit.left()
            
@mod.action_class
class module_actions:
    def join_tables(text: str):
        """Inserts a JOIN statement"""
        text = " ".join([text, "JOIN  ON"])
        actions.insert(text)
        actions.edit.left()
        actions.edit.left()
        actions.edit.left()