from talon import Context, Module, actions, settings

mod = Module()
ctx = Context()
ctx.matches = """
tag: user.julia
"""

ctx.lists["user.code_common_function"] = {
    "print": "print",
}

ctx.lists["user.code_type"] = {
    "integer": "Int",
}

@ctx.action_class("user")
class UserActions:
    def code_operator_subscript():
        actions.user.insert_between("[", "]")

    def code_insert_null():
        actions.auto_insert("nothing")

    def code_state_if():
        actions.auto_insert("if\nend")
        actions.key("tab")
        actions.edit.up()
        actions.edit.line_end()
        actions.insert(" ")

    def code_state_else():
        actions.auto_insert("else")
        actions.key("enter")
    def code_state_else_if(): actions.auto_insert("elseif ")

    def code_state_return():
        actions.insert("return ")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_default_function(text: str):
        actions.user.code_public_function(text)

    def code_public_function(text: str):
        result = "function {}()\nend".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.key("tab")              # auto-indent 'end'
        actions.edit.up()
        actions.edit.line_end()
        actions.edit.left()

    def code_operator_modulo(): actions.auto_insert(" % ")
    def code_operator_modulo_assignment(): actions.auto_insert(" %= ")
    def code_operator_equal(): actions.auto_insert(" == ")
    def code_operator_not_equal(): actions.auto_insert(" != ")
    def code_operator_greater_than(): actions.auto_insert(" > ")
    def code_operator_greater_than_or_equal_to(): actions.auto_insert(" >= ")
    def code_operator_less_than(): actions.auto_insert(" < ")
    def code_operator_less_than_or_equal_to(): actions.auto_insert(" <= ")
    def code_operator_and(): actions.auto_insert(" && ")
    def code_operator_or(): actions.auto_insert(" || ")
    def code_operator_in(): actions.auto_insert(" ∈ ")
    def code_operator_not_in(): actions.auto_insert(" ∉ ")


def julia_end():
    actions.insert("\nend")
    actions.key("tab")                  #auto indent
    actions.edit.up()
    actions.edit.line_end()

def julia_end_below():
    actions.insert("end")
    actions.edit.line_insert_up()
