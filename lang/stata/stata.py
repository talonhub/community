from talon import Context, actions, settings

ctx = Context()

ctx.matches = r"""
code.language: stata
"""

# functions.py
ctx.lists["user.code_parameter_name"] = {
    # regressions
    "V C E cluster": "vce(cluster)",
    "V C E robust": "vce(robust)",
}

# functions_common.py
ctx.lists["user.code_common_function"] = {
    # base stata
    "global": "global",
    "local": "local",
    "reg": "reg",
    "regress": "reg",
    # packages
    "estadd": "estadd",
    "estout": "estout",
    "estpost": "estpost",
    "eststo": "eststo",
    "esttab": "esttab",
}

# libraries.py
ctx.lists["user.code_libraries"] = {
    "estout": "estout",
}


@ctx.action_class("user")
class UserActions:
    # comment_line.py
    def code_comment_line_prefix():
        actions.auto_insert("* ")

    # functions.py
    def code_private_function(text: str):
        result = "program {} \n\nend".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.up()
        actions.key("tab")

    def code_default_function(text: str):
        actions.user.code_private_function(text)

    def code_insert_named_argument(parameter_name: str):
        actions.insert(f"{parameter_name} ")

    # functions_common.py
    def code_insert_function(text: str, selection: str):
        text += f" {selection or ''}"
        actions.user.paste(text)

    # imperative.py
    def code_block():
        actions.auto_insert("\n")

    def code_state_if():
        actions.insert("if  {\n\n}")
        actions.key("up tab up")
        actions.edit.line_end()
        actions.key("left:2")

    def code_state_else_if():
        actions.insert("else if  {\n\n}")
        actions.key("up tab up")
        actions.edit.line_end()
        actions.key("left:2")

    def code_state_else():
        actions.insert("else {\n\n}")
        actions.key("up tab")

    def code_state_for():
        actions.insert("forval  {\n\n}")
        actions.key("up tab up")
        actions.edit.line_end()
        actions.key("left:2")

    def code_state_for_each():
        actions.insert("foreach  in  {\n\n}")
        actions.key("up tab up")
        actions.edit.line_end()
        actions.key("left:2")

    def code_state_while():
        actions.insert("while  {\n\n}")
        actions.key("up tab up")
        actions.edit.line_end()
        actions.key("left:2")

    def code_break():
        actions.insert("break")

    def code_next():
        actions.insert("continue")

    # libraries.py
    def code_import():
        actions.auto_insert("ssc install ")

    # libraries.py
    def code_insert_library(text: str, selection: str):
        actions.auto_insert("ssc install ")
        actions.user.paste(text + selection)

    # operators_array.py
    def code_operator_subscript():
        actions.user.insert_between("[", "]")

    # operators_assignment.py
    def code_operator_assignment():
        actions.auto_insert(" = ")

    # operators_math.py
    def code_operator_subtraction():
        actions.auto_insert(" - ")

    def code_operator_addition():
        actions.auto_insert(" + ")

    def code_operator_multiplication():
        actions.auto_insert(" * ")

    def code_operator_division():
        actions.auto_insert(" / ")

    def code_operator_modulo():
        actions.user.insert_between("mod(", ")")

    def code_operator_exponent():
        actions.auto_insert(" ^ ")

    def code_operator_equal():
        actions.auto_insert(" == ")

    def code_operator_not_equal():
        actions.auto_insert(" != ")

    def code_operator_greater_than():
        actions.auto_insert(" > ")

    def code_operator_less_than():
        actions.auto_insert(" < ")

    def code_operator_greater_than_or_equal_to():
        actions.auto_insert(" >= ")

    def code_operator_less_than_or_equal_to():
        actions.auto_insert(" <= ")

    def code_operator_and():
        actions.auto_insert(" & ")

    def code_operator_or():
        actions.auto_insert(" | ")
