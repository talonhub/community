from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()
ctx.matches = r"""
mode: user.java
mode: user.auto_lang
and code.language: java
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

mod.list("java_boxed_types", desc="Java Boxed Types")
ctx.lists["self.java_boxed_types"] = java_boxed_types

# Common Classes
java_common_classes = {
    "Object": "Object",
    "string": "String",
    "thread": "Thread",
    "exception": "Exception",
}

mod.list("java_common_classes", desc="Java Common Classes")
ctx.lists["self.java_common_classes"] = java_common_classes



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

mod.list("java_generic_data_structures", desc="Java Generic Data Structures")
ctx.lists["self.java_generic_data_structures"] = java_generic_data_structures

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

mod.list("java_modifiers", desc="Java Modifiers")
ctx.lists["self.java_modifiers"] = java_modifiers

@ctx.action_class("user")
class UserActions:
    def code_operator_indirection():
        actions.skip()

    def code_operator_address_of():
        actions.skip()

    def code_operator_lambda():
        actions.auto_insert(" -> ")

    def code_operator_subscript():
        actions.insert("[]")
        actions.key("left")

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

    def code_null():
        actions.auto_insert("null")

    def code_is_null():
        actions.auto_insert(" == null")

    def code_is_not_null():
        actions.auto_insert(" != null")

    def code_state_if():
        actions.insert("if () ")
        actions.key("left")
        actions.key("left")

    def code_state_else_if():
        actions.insert("else if () ")
        actions.key("left")
        actions.key("left")

    def code_state_else():
        actions.insert("else ")
        actions.key("enter")

    def code_state_switch():
        actions.insert("switch () ")
        actions.key("left")
        actions.edit.left()

    def code_state_case():
        actions.insert("case \nbreak;")
        actions.edit.up()

    def code_state_for():
        actions.insert("for () ")
        actions.key("left")
        actions.key("left")

    def code_state_while():
        actions.insert("while () ")
        actions.edit.left()
        actions.edit.left()

    def code_break():           
        actions.auto_insert('break;')

    def code_next():
        actions.auto_insert('continue;')
    
    def code_true():          
        actions.auto_insert('true')

    def code_false():           
        actions.auto_insert('false')

    def code_type_class():
        actions.auto_insert("class ")

    def code_import():         
        actions.auto_insert("import ")

    def code_private_function(text: str):
        actions.insert("private")

    def code_protected_function(text: str):
        actions.user.code_private_function()

    def code_public_function(text: str):
        actions.insert("public ")

    def code_state_return():
        actions.insert("return ")

    def code_comment(): 
        actions.auto_insert('// ')

    def code_block_comment():
        actions.insert('/*')
        actions.key('enter')
        actions.key('enter')
        actions.insert('*/')
        actions.edit.up()

    def code_block_comment_prefix(): 
        actions.auto_insert('/*')

    def code_block_comment_suffix(): 
        actions.auto_insert('*/')

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"

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