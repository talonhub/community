from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()
ctx.matches = r"""
tag: user.java
"""
ctx.tags = ["user.code_operators", "user.code_generic"]

# Primitive Types
java_primitive_types = {
    "boolean": "boolean",
    "int": "int",
    "float": "float",
    "byte": "byte",
    "double": "double",
    "short": "short",
    "long": "long",
    "char": "char",
    "void": "void",
}

# Java Boxed Types
java_boxed_types = {
    "Byte": "Byte",
    "Integer": "Integer",
    "Double": "Double",
    "Short": "Short",
    "Float": "Float",
    "Long": "Long",
    "Boolean": "Boolean",
    "Character": "Character",
    "Void": "Void",
}

mod.list("java_boxed_type", desc="Java Boxed Types")
ctx.lists["self.java_boxed_type"] = java_boxed_types

# Common Classes
java_common_classes = {
    "Object": "Object",
    "string": "String",
    "thread": "Thread",
    "exception": "Exception",
}

mod.list("java_common_class", desc="Java Common Classes")
ctx.lists["self.java_common_class"] = java_common_classes


# Java Generic Data Structures
java_generic_data_structures = {
    # Interfaces
    "set": "Set",
    "list": "List",
    "queue": "Queue",
    "deque": "Deque",
    "map": "Map",
    # Classes
    "hash set": "HashSet",
    "array list": "ArrayList",
    "hash map": "HashMap",
}

unboxed_types = java_primitive_types.copy()
unboxed_types.update(java_common_classes)
unboxed_types.update(java_generic_data_structures)

ctx.lists["user.code_type"] = unboxed_types

mod.list("java_generic_data_structure", desc="Java Generic Data Structures")
ctx.lists["self.java_generic_data_structure"] = java_generic_data_structures

# Java Modifies
java_modifiers = {
    "public": "public",
    "private": "private",
    "protected": "protected",
    "static": "static",
    "synchronized": "synchronized",
    "volatile": "volatile",
    "transient": "transient",
    "abstract": "abstract",
    "interface": "interface",
    "final": "final",
}

mod.list("java_modifier", desc="Java Modifiers")
ctx.lists["self.java_modifier"] = java_modifiers


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

    def code_self():
        actions.insert("this")

    def code_operator_object_accessor():
        actions.insert(".")

    def code_insert_null():
        actions.insert("null")

    def code_insert_is_null():
        actions.insert(" == null")

    def code_insert_is_not_null():
        actions.insert(" != null")

    def code_state_if():
        actions.user.insert_between("if (", ") ")

    def code_state_else_if():
        actions.user.insert_between("else if (", ") ")

    def code_state_else():
        actions.insert("else ")
        actions.key("enter")

    def code_state_switch():
        actions.user.insert_between("switch (", ") ")

    def code_state_case():
        actions.insert("case \nbreak;")
        actions.edit.up()

    def code_state_for():
        actions.user.insert_between("for (", ") ")

    def code_state_while():
        actions.user.insert_between("while (", ") ")

    def code_break():
        actions.insert("break;")

    def code_next():
        actions.insert("continue;")

    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

    def code_define_class():
        actions.insert("class ")

    def code_import():
        actions.insert("import ")

    def code_private_function(text: str):
        actions.insert("private")

    def code_protected_function(text: str):
        actions.user.code_private_function()

    def code_public_function(text: str):
        actions.insert("public ")

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
        result = "private void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_private_static_function(text: str):
        """Inserts private static function"""
        result = "private static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_protected_function(text: str):
        result = "void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_protected_static_function(text: str):
        result = "static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_public_function(text: str):
        result = "public void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_public_static_function(text: str):
        result = "public static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)
