from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()
ctx.matches = r"""
code.language: go
"""

# Primitive Types
ctx.lists["self.code_type"] = {
    "boolean": "bool",
    "int": "int",
    "float": "float",
    "byte": "byte",
    "double": "double",
    "short": "short",
    "long": "long",
    "char": "char",
    "string": "string",
    "rune": "rune",
    "void": "void",
    "channel": "channel",
}

ctx.lists["user.code_keyword"] = {
    "break": "break",
    "continue": "continue",
    "struct": "struct",
    "type": "type",
    "return": "return",
    "package": "package",
    "import": "import",
    "null": "nil",
    "nil": "nil",
    "true": "true",
    "false": "false",
    "defer": "defer",
    "go": "go",
    "if": "if",
    "else": "else",
    "switch": "switch",
    "select": "select",
    "const": "const",
}

ctx.lists["user.code_common_function"] = {
    # golang buildin functions
    "append": "append",
    "length": "len",
    "make": "make",
    # formatting
    "format print": "fmt.Printf",
    "format sprint": "fmt.Sprintf",
    "format print line": "fmt.Println",
    # time
    "time hour": "time.Hour",
    "time minute": "time.Minute",
    "time second": "time.Second",
    "time millisecond": "time.Millisecond",
    "time microsecond": "time.Microsecond",
    "time nanosecond": "time.Nanosecond",
    # IO
    "buf I O": "bufio.",
    # strings
    "string convert": "strconv.",
    "string convert to int": "strconv.AtoI",
}


@ctx.action_class("user")
class UserActions:
    def code_operator_lambda():
        actions.insert(" -> ")

    def code_operator_subscript():
        actions.user.insert_between("[", "]")

    def code_operator_assignment():
        actions.insert(" = ")

    def code_operator_subtraction():
        actions.insert(" - ")

    def code_operator_subtraction_assignment():
        actions.insert(" -= ")

    def code_operator_addition():
        actions.insert(" + ")

    def code_operator_addition_assignment():
        actions.insert(" += ")

    def code_operator_multiplication():
        actions.insert(" * ")

    def code_operator_multiplication_assignment():
        actions.insert(" *= ")

    def code_operator_exponent():
        actions.insert(" ^ ")

    def code_operator_division():
        actions.insert(" / ")

    def code_operator_division_assignment():
        actions.insert(" /= ")

    def code_operator_modulo():
        actions.insert(" % ")

    def code_operator_modulo_assignment():
        actions.insert(" %= ")

    def code_operator_equal():
        actions.insert(" == ")

    def code_operator_not_equal():
        actions.insert(" != ")

    def code_operator_greater_than():
        actions.insert(" > ")

    def code_operator_greater_than_or_equal_to():
        actions.insert(" >= ")

    def code_operator_less_than():
        actions.insert(" < ")

    def code_operator_less_than_or_equal_to():
        actions.insert(" <= ")

    def code_operator_and():
        actions.insert(" && ")

    def code_operator_or():
        actions.insert(" || ")

    def code_operator_bitwise_and():
        actions.insert(" & ")

    def code_operator_bitwise_and_assignment():
        actions.insert(" &= ")

    def code_operator_increment():
        actions.insert("++")

    def code_operator_bitwise_or():
        actions.insert(" | ")

    def code_operator_bitwise_exclusive_or():
        actions.insert(" ^ ")

    def code_operator_bitwise_left_shift():
        actions.insert(" << ")

    def code_operator_bitwise_left_shift_assignment():
        actions.insert(" <<= ")

    def code_operator_bitwise_right_shift():
        actions.insert(" >> ")

    def code_operator_bitwise_right_shift_assignment():
        actions.insert(" >>= ")

    def code_operator_indirection():
        actions.insert("*")

    def code_operator_address_of():
        actions.insert("&")

    def code_self():
        actions.insert("this")

    def code_operator_object_accessor():
        actions.insert(".")

    def code_insert_null():
        actions.insert("nil")

    def code_insert_is_null():
        actions.insert(" == nil")

    def code_insert_is_not_null():
        actions.insert(" != nil")

    def code_state_if():
        actions.user.insert_between("if ", " ")

    def code_state_else_if():
        actions.user.insert_between("else if ", " ")

    def code_state_else():
        actions.insert("else ")
        actions.key("enter")

    def code_state_switch():
        actions.user.insert_between("switch ", " ")

    def code_state_case():
        actions.user.insert_between("case ", ":")

    def code_state_for():
        actions.user.insert_between("for ", " ")

    # There is no while keyword in go. Closest approximation is a for loop.
    def code_state_while():
        actions.user.insert_between("for ", " ")

    def code_break():
        actions.insert("break")

    def code_next():
        actions.insert("continue")

    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

    def code_import():
        actions.insert("import ")

    def code_state_return():
        actions.insert("return ")

    def code_comment_line_prefix():
        actions.insert("// ")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "func {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)
