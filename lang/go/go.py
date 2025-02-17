from talon import Context, Module, actions, settings

from ..tags.operators import Operators

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

operators = Operators(
    LAMBDA=" -> ",
    SUBSCRIPT="]",
    ASSIGNMENT=" = ",
    MATH_SUBTRACT=" - ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    MATH_ADD=" + ",
    ASSIGNMENT_ADDITION=" += ",
    MATH_MULTIPLY=" * ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    MATH_EXPONENT=" ^ ",
    MATH_DIVIDE=" / ",
    ASSIGNMENT_DIVISION=" /= ",
    MATH_MODULO=" % ",
    ASSIGNMENT_MODULO=" %= ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" && ",
    MATH_OR=" || ",
    BITWISE_AND=" & ",
    ASSIGNMENT_BITWISE_AND=" &= ",
    ASSIGNMENT_INCREMENT="++",
    BITWISE_OR=" | ",
    BITWISE_EXCLUSIVE_OR=" ^ ",
    BITWISE_LEFT_SHIFT=" << ",
    ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
    BITWISE_RIGHT_SHIFT=" >> ",
    ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
    POINTER_INDIRECTION="*",
    POINTER_ADDRESS_OF="&",
)

@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

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
