from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()
ctx.matches = r"""
tag: user.scala
"""

# Scala Common Types
scala_common_types = {
    "Byte": "Byte",
    "Int": "Int",
    "Double": "Double",
    "Short": "Short",
    "Float": "Float",
    "Long": "Long",
    "Boolean": "Boolean",
    "Char": "Char",
    "String": "String",
    "None": "None"
}

# Scala Common Generic Types
scala_common_generic_types = {
    "seq": "Seq",
    "set": "Set",
    "list": "List",
    "array": "Array",
    "map": "Map",
    "stack": "Stack"
}

scala_types = scala_common_types.copy()
scala_types.update(scala_common_generic_types)
ctx.lists["user.code_type"] = scala_types

@ctx.action_class("user")
class UserActions:
    def code_block():
        actions.insert('{}')
        actions.edit.left()
        actions.key('enter')

    def code_operator_lambda():
        actions.auto_insert(" => ")

    def code_operator_subscript():
        actions.insert("()")
        actions.edit.left()

    def code_operator_assignment():
        actions.auto_insert(" = ")

    def code_operator_subtraction():
        actions.insert(" - ")

    def code_operator_subtraction_assignment():
        actions.auto_insert(" -= ")

    def code_operator_addition():
        actions.auto_insert(" + ")

    def code_operator_addition_assignment():
        actions.auto_insert(" += ")

    def code_operator_multiplication():
        actions.auto_insert(" * ")

    def code_operator_multiplication_assignment():
        actions.auto_insert(" *= ")

    def code_operator_exponent():
        actions.auto_insert(" ^ ")

    def code_operator_division():
        actions.auto_insert(" / ")

    def code_operator_division_assignment():
        actions.auto_insert(" /= ")

    def code_operator_modulo():
        actions.auto_insert(" % ")

    def code_operator_modulo_assignment():
        actions.auto_insert(" %= ")

    def code_operator_equal():
        actions.auto_insert(" == ")

    def code_operator_not_equal():
        actions.auto_insert(" != ")

    def code_operator_greater_than():
        actions.auto_insert(" > ")

    def code_operator_greater_than_or_equal_to():
        actions.auto_insert(" >= ")

    def code_operator_less_than():
        actions.auto_insert(" < ")

    def code_operator_less_than_or_equal_to():
        actions.auto_insert(" <= ")

    def code_operator_and():
        actions.auto_insert(" && ")

    def code_operator_or():
        actions.auto_insert(" || ")

    def code_operator_bitwise_and():
        actions.auto_insert(" & ")

    def code_operator_bitwise_and_assignment():
        actions.auto_insert(' &= ')

    def code_operator_increment():
        actions.auto_insert('++')

    def code_operator_bitwise_or():
        actions.auto_insert(" | ")

    def code_operator_bitwise_exclusive_or():
        actions.auto_insert(" ^ ")

    def code_operator_bitwise_left_shift():
        actions.auto_insert(" << ")

    def code_operator_bitwise_left_shift_assignment():
        actions.auto_insert(" <<= ")

    def code_operator_bitwise_right_shift():
        actions.auto_insert(" >> ")

    def code_operator_bitwise_right_shift_assignment():
        actions.auto_insert(" >>= ")

    def code_self():
        actions.auto_insert("this")

    def code_insert_null():
        actions.auto_insert("null")

    def code_insert_is_null():
        actions.auto_insert(" == null")

    def code_insert_is_not_null():
        actions.auto_insert(" != null")

    def code_state_if():
        actions.insert("if () ")
        actions.edit.left()
        actions.edit.left()

    def code_state_else_if():
        actions.insert("else if () ")
        actions.edit.left()
        actions.edit.left()

    def code_state_else():
        actions.insert("else ")
        actions.key("enter")

    def code_state_switch():
        actions.insert("match {\n")

    def code_state_case():
        actions.insert("case  => ")
        actions.edit.left()
        actions.edit.left()
        actions.edit.left()
        actions.edit.left()

    def code_state_for():
        actions.insert("for () ")
        actions.edit.left()
        actions.edit.left()

    def code_state_while():
        actions.insert("while () ")
        actions.edit.left()
        actions.edit.left()

    def code_break():
        actions.auto_insert('break')

    def code_next():
        actions.auto_insert('continue')

    def code_insert_true():
        actions.auto_insert('true')

    def code_insert_false():
        actions.auto_insert('false')

    def code_define_class():
        actions.auto_insert("class ")

    def code_import():
        actions.auto_insert("import ")

    def code_state_return():
        actions.insert("return ")

    def code_comment_line_prefix():
        actions.auto_insert('// ')

    def code_comment_block():
        actions.insert('/*')
        actions.key('enter')
        actions.key('enter')
        actions.insert('*/')
        actions.edit.up()

    def code_comment_block_prefix():
        actions.auto_insert('/*')

    def code_comment_block_suffix():
        actions.auto_insert('*/')

    def code_insert_type_annotation(type: str):
        actions.insert(f": {type}")

    def code_insert_return_type(type: str):
        actions.insert(f": {type}")

    def code_operator_object_accessor():
        actions.insert(".")

    def code_default_function(text: str):
        """Inserts function declaration"""
        actions.user.code_public_function(text)

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "private def {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_protected_function(text: str):
        result = "protected def {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_public_function(text: str):
        result = "def {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)
