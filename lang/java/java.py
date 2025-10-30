from contextlib import suppress

from talon import Context, Module, actions, settings

from ...core.described_functions import create_described_insert_between
from ..tags.operators import Operators

ctx = Context()
mod = Module()
ctx.matches = r"""
code.language: java
"""

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

operators = Operators(
    # code_operators_array
    SUBSCRIPT=create_described_insert_between("[", "]"),
    # code_operators_assignment
    ASSIGNMENT=" = ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    ASSIGNMENT_ADDITION=" += ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    ASSIGNMENT_DIVISION=" /= ",
    ASSIGNMENT_MODULO=" %= ",
    ASSIGNMENT_INCREMENT="++",
    ASSIGNMENT_BITWISE_AND=" &= ",
    ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
    ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
    # code_operators_bitwise
    BITWISE_AND=" & ",
    BITWISE_OR=" | ",
    BITWISE_EXCLUSIVE_OR=" ^ ",
    BITWISE_LEFT_SHIFT=" << ",
    BITWISE_RIGHT_SHIFT=" >> ",
    # code_operators_lambda
    LAMBDA=" -> ",
    # code_operators_math
    MATH_SUBTRACT=" - ",
    MATH_ADD=" + ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    MATH_EXPONENT=" ^ ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" && ",
    MATH_OR=" || ",
    MATH_NOT="!",
)


def public_camel_case_format_variable(variable: str):
    return actions.user.formatted_text(variable, "PUBLIC_CAMEL_CASE")


# This is not part of the long term stable API
# After we implement generics support for several languages,
# we plan on abstracting out from the specific implementations into a general grammar


@mod.capture(rule="{user.java_boxed_type} | <user.text>")
def java_type_parameter_argument(m) -> str:
    """A Java type parameter for a generic data structure"""
    with suppress(AttributeError):
        return m.java_boxed_type
    return public_camel_case_format_variable(m.text)


@mod.capture(rule="<user.java_generic_type> stop | <user.java_type_parameter_argument>")
def java_recursive_type_parameter_argument(m) -> str:
    """Either a nested java generic type or a concrete type"""
    with suppress(AttributeError):
        return m.java_generic_type
    return m.java_type_parameter_argument


@mod.capture(
    rule="(<user.java_generic_data_structure> of)+ (<user.java_generic_type_parameter_arguments>) [stop]"
)
def java_generic_type_tail(m) -> str:
    """Supports nesting generic data structures at the end of a generic type without needing the stop word"""
    nested_structures = m.java_generic_data_structure_list
    parameter_arguments = m.java_generic_type_parameter_arguments
    return (
        "<".join(nested_structures)
        + "<"
        + ", ".join(parameter_arguments)
        + ">" * len(nested_structures)
    )


@mod.capture(rule="[type] {user.java_generic_data_structure} | type <user.text>")
def java_generic_data_structure(m) -> str:
    """A Java generic data structure that takes type parameter arguments"""
    with suppress(AttributeError):
        return m.java_generic_data_structure
    return public_camel_case_format_variable(m.text)


@mod.capture(rule="(and <user.java_recursive_type_parameter_argument>)+")
def java_generic_type_parameter_additional_arguments(m) -> list[str]:
    """Additional Java type parameters"""
    return m.java_recursive_type_parameter_argument_list


@mod.capture(
    rule="<user.java_recursive_type_parameter_argument> [<user.java_generic_type_parameter_additional_arguments>]"
)
def java_generic_type_parameter_arguments(m) -> list[str]:
    """A list of Java type parameters"""
    result = [m.java_recursive_type_parameter_argument]
    with suppress(AttributeError):
        result.extend(m.java_generic_type_parameter_additional_arguments)
    return result


@mod.capture(
    rule="<user.java_generic_data_structure> of <user.java_generic_type_parameter_arguments>"
)
def java_generic_type(m) -> str:
    """A generic type with specific type parameters"""
    parameters = m.java_generic_type_parameter_arguments
    parameter_text = ", ".join(parameters)
    return f"{m.java_generic_data_structure}<{parameter_text}>"


@mod.capture(
    rule="(<user.java_generic_data_structure> of <user.java_generic_type_parameter_arguments>) | (<user.java_generic_data_structure> of <user.java_generic_type_tail>) | (<user.java_generic_data_structure> of <user.java_generic_type_parameter_arguments> and <user.java_generic_type_tail>)"
)
def java_generic_type_spoken_form(m) -> str:
    """The full spoken form for a java generic type"""
    parameters = []
    with suppress(AttributeError):
        parameters.extend(m.java_generic_type_parameter_arguments)
    with suppress(AttributeError):
        parameters.append(m.java_generic_type_tail)
    parameter_text = ", ".join(parameters)
    return f"{m.java_generic_data_structure}<{parameter_text}>"


# End of unstable section


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

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

    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

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
