from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()
ctx.matches = r"""
tag: user.scala
"""

# Scala Common Types
scala_common_types = {
    "boolean": "Boolean",
    "int": "Int",
    "float": "Float",
    "byte": "Byte",
    "double": "Double",
    "short": "Short",
    "long": "Long",
    "char": "Char",
    "unit": "Unit",
    "any": "Any",
    "any val": "AnyVal",
    "string": "String",
    "thread": "Thread",
    "exception": "Exception",
    "throwable": "Throwable",
    "none": "None",
    "success": "Success",
    "failure": "Failure",
}

# Scala Common Generic Types
scala_common_generic_types = {
    "array": "Array",
    "deck": "Deque",
    "future": "Future",
    "list": "List",
    "map": "Map",
    "nil": "Nil",
    "option": "Option",
    "queue": "Queue",
    "seek": "Seq",
    "set": "Set",
    "some": "Some",
    "stack": "Stack",
    "try": "Try",
}

scala_types = scala_common_types.copy()
scala_types.update(scala_common_generic_types)
ctx.lists["user.code_type"] = scala_types

# Scala Modifies
scala_modifiers = {
    "public": "public",
    "private": "private",
    "protected": "protected",
}

mod.list("scala_modifier", desc="Scala Modifiers")
ctx.lists["user.scala_modifier"] = scala_modifiers

scala_keywords = {
    "abstract": "abstract",
    "case class": "case class",
    "def": "def",
    "extends": "extends",
    "implicit": "implicit",
    "lazy val": "lazy val",
    "new": "new",
    "object": "object",
    "override": "override",
    "package": "package",
    "sealed": "sealed",
    "throw": "throw",
    "trait": "trait",
    "type": "type",
    "val": "val",
    "var": "var",
    "with": "with",
    "yield": "yield",
}

mod.list("scala_keyword", desc="Scala Keywords")
ctx.lists["user.scala_keyword"] = scala_keywords

@ctx.action_class("user")
class UserActions:
    def code_block():
        actions.insert('{}')
        actions.edit.left()
        actions.key('enter')

    def code_operator_lambda():
        actions.insert(" => ")

    def code_operator_subscript():
        actions.insert("()")
        actions.edit.left()

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
        actions.insert(' &= ')

    def code_operator_increment():
        actions.insert('++')

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

    def code_self():
        actions.insert("this")

    def code_insert_null():
        actions.insert("null")

    def code_insert_is_null():
        actions.insert(" == null")

    def code_insert_is_not_null():
        actions.insert(" != null")

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
        actions.insert('break')

    def code_next():
        actions.insert('continue')

    def code_insert_true():
        actions.insert('true')

    def code_insert_false():
        actions.insert('false')

    def code_define_class():
        actions.insert("class ")

    def code_import():
        actions.insert("import ")

    def code_state_return():
        actions.insert("return ")

    def code_comment_line_prefix():
        actions.insert('// ')

    def code_comment_block():
        actions.insert('/*')
        actions.key('enter')
        actions.key('enter')
        actions.insert('*/')
        actions.edit.up()

    def code_comment_block_prefix():
        actions.insert('/*')

    def code_comment_block_suffix():
        actions.insert('*/')

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
