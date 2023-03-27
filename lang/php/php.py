from talon import Context, actions, settings

ctx = Context()
ctx.matches = r"""
tag: user.php
"""

ctx.lists["user.code_type"] = {
    "int": "int",
    "float": "float",
    "string": "string",
    "bool": "bool",
    "array": "array",
    "null": "null",
    "void": "void",
}


@ctx.action_class("user")
class UserActions:
    def code_self():
        actions.auto_insert("$this")

    def code_operator_object_accessor():
        actions.auto_insert("->")

    def code_define_class():
        actions.auto_insert("class ")

    def code_block():
        actions.insert("{}")
        actions.edit.left()
        actions.key("enter")

    def code_import():
        actions.auto_insert("use ;")
        actions.edit.left()

    def code_comment_line_prefix():
        actions.auto_insert("// ")

    def code_comment_block():
        actions.user.code_comment_block_prefix()
        actions.key("enter")
        actions.key("enter")
        actions.user.code_comment_block_suffix()
        actions.edit.up()

    def code_comment_block_prefix():
        actions.auto_insert("/*")

    def code_comment_block_suffix():
        actions.auto_insert("*/")

    def code_comment_documentation():
        actions.insert("/**")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_insert_null():
        actions.auto_insert("null")

    def code_insert_is_null():
        actions.auto_insert("is_null()")
        actions.edit.left()

    def code_insert_is_not_null():
        actions.auto_insert("isset()")
        actions.edit.left()

    def code_operator_assignment():
        actions.auto_insert(" = ")

    def code_operator_subtraction():
        actions.auto_insert(" - ")

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
        actions.auto_insert(" ** ")

    def code_operator_division():
        actions.auto_insert(" / ")

    def code_operator_division_assignment():
        actions.auto_insert(" /= ")

    def code_operator_modulo():
        actions.auto_insert(" % ")

    def code_operator_modulo_assignment():
        actions.auto_insert(" %= ")

    def code_operator_equal():
        actions.auto_insert(" === ")

    def code_operator_not_equal():
        actions.auto_insert(" !== ")

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

    def code_state_if():
        actions.insert("if ()")
        actions.edit.left()

    def code_state_else_if():
        actions.insert("elseif ()")
        actions.edit.left()

    def code_state_else():
        actions.insert("else {")
        actions.key("enter")

    def code_state_while():
        actions.insert("while ()")
        actions.edit.left()

    def code_state_for():
        actions.insert("for ()")
        actions.edit.left()

    def code_state_for_each():
        actions.insert("foreach ()")
        actions.edit.left()

    def code_state_switch():
        actions.insert("switch ()")
        actions.edit.left()

    def code_state_case():
        actions.insert("case :")
        actions.edit.left()

    def code_state_do():
        actions.insert("do {")
        actions.key("enter")

    def code_state_go_to():
        actions.insert("goto ;")
        actions.edit.left()

    def code_state_return():
        actions.insert("return ;")
        actions.edit.left()

    def code_break():
        actions.insert("break;")

    def code_next():
        actions.insert("continue;")

    def code_default_function(text: str):
        actions.user.code_public_function(text)

    def code_protected_function(text: str):
        """Inserts protected function declaration"""
        result = "protected function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_public_function(text: str):
        """Inserts public function declaration"""
        result = "public function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "private function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_private_static_function(text: str):
        """Inserts private static function declaration"""
        result = "private static function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_protected_static_function(text: str):
        """Inserts protected static function declaration"""
        result = "protected static function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_public_static_function(text: str):
        """Inserts public static function declaration"""
        result = "public static function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_insert_return_type(type: str):
        actions.insert(f": {type}")
