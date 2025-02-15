from typing import Callable, TypedDict

from talon import Module, actions

mod = Module()

mod.tag("code_operators_array", desc="Tag for enabling array operator commands")
mod.tag("code_operators_assignment", desc="Tag for enabling assignment commands")
mod.tag("code_operators_bitwise", desc="Tag for enabling bitwise operator commands")
mod.tag(
    "code_operators_lambda", desc="Tag for enabling commands for anonymous functions"
)
mod.tag("code_operators_math", desc="Tag for enabling mathematical operator commands")
mod.tag("code_operators_pointer", desc="Tag for enabling pointer operator commands")

mod.list("code_operators_array", desc="List of code operators for arrays")
mod.list("code_operators_assignment", desc="List of code operators for assignments")
mod.list("code_operators_bitwise", desc="List of code operators for bitwise operations")
mod.list("code_operators_lambda", desc="List of code operators for anonymous functions")
mod.list(
    "code_operators_math",
    desc="List of code operators for mathematical operations",
)
mod.list(
    "code_operators_math_comparison",
    desc="List of code operators for mathematical comparison operations",
)
mod.list("code_operators_pointer", desc="List of code operators for pointers")


Operator = str | Callable[[], None]


class Operators(TypedDict, total=False):
    # code_operators_array
    SUBSCRIPT: Operator

    # code_operators_assignment
    ASSIGNMENT: Operator
    ASSIGNMENT_OR: Operator
    ASSIGNMENT_SUBTRACTION: Operator
    ASSIGNMENT_ADDITION: Operator
    ASSIGNMENT_MULTIPLICATION: Operator
    ASSIGNMENT_DIVISION: Operator
    ASSIGNMENT_MODULO: Operator
    ASSIGNMENT_INCREMENT: Operator
    ASSIGNMENT_BITWISE_AND: Operator
    ASSIGNMENT_BITWISE_OR: Operator
    ASSIGNMENT_BITWISE_EXCLUSIVE_OR: Operator
    ASSIGNMENT_BITWISE_LEFT_SHIFT: Operator
    ASSIGNMENT_BITWISE_RIGHT_SHIFT: Operator

    # code_operators_bitwise
    BITWISE_AND: Operator
    BITWISE_OR: Operator
    BITWISE_NOT: Operator
    BITWISE_EXCLUSIVE_OR: Operator
    BITWISE_LEFT_SHIFT: Operator
    BITWISE_RIGHT_SHIFT: Operator

    # code_operators_lambda
    LAMBDA: Operator

    # code_operators_math
    MATH_SUBTRACT: Operator
    MATH_ADD: Operator
    MATH_MULTIPLY: Operator
    MATH_DIVIDE: Operator
    MATH_MODULO: Operator
    MATH_EXPONENT: Operator
    MATH_EQUAL: Operator
    MATH_NOT_EQUAL: Operator
    MATH_GREATER_THAN: Operator
    MATH_GREATER_THAN_OR_EQUAL: Operator
    MATH_LESS_THAN: Operator
    MATH_LESS_THAN_OR_EQUAL: Operator
    MATH_AND: Operator
    MATH_OR: Operator
    MATH_NOT: Operator
    MATH_IN: Operator
    MATH_NOT_IN: Operator

    # code_operators_pointer
    POINTER_INDIRECTION: Operator
    POINTER_ADDRESS_OF: Operator
    POINTER_STRUCTURE_DEREFERENCE: Operator


@mod.action_class
class Actions:
    def code_operator(identifier: str):
        """Insert a code operator"""
        try:
            operators: Operators = actions.user.code_get_operators()
            operator = operators.get(identifier)

            if operator is None:
                raise ValueError(f"Operator {identifier} not found")

            if callable(operator):
                operator()
            else:
                actions.insert(operator)
        except NotImplementedError:
            # This language has not implement the operators dict and we therefore use the fallback
            operators_fallback(identifier)
            return

    def code_get_operators() -> Operators:
        """Get code operators dictionary"""


# Fallback is to rely on the legacy actions
def operators_fallback(identifier: str) -> None:
    match identifier:
        # code_operators_array
        case "SUBSCRIPT":
            actions.user.code_operator_subscript()

        # code_operators_assignment
        case "ASSIGNMENT":
            actions.user.code_operator_assignment()
        case "ASSIGNMENT_OR":
            actions.user.code_or_operator_assignment()
        case "ASSIGNMENT_SUBTRACTION":
            actions.user.code_operator_subtraction_assignment()
        case "ASSIGNMENT_ADDITION":
            actions.user.code_operator_addition_assignment()
        case "ASSIGNMENT_MULTIPLICATION":
            actions.user.code_operator_multiplication_assignment()
        case "ASSIGNMENT_MODULO":
            actions.user.code_operator_modulo_assignment()
        case "ASSIGNMENT_INCREMENT":
            actions.user.code_operator_increment()
        case "ASSIGNMENT_BITWISE_AND":
            actions.user.code_operator_bitwise_and_assignment()
        case "ASSIGNMENT_BITWISE_OR":
            actions.user.code_operator_bitwise_or_assignment()
        case "ASSIGNMENT_BITWISE_EXCLUSIVE_OR":
            actions.user.code_operator_bitwise_exclusive_or_assignment()
        case "ASSIGNMENT_BITWISE_LEFT_SHIFT":
            actions.user.code_operator_bitwise_left_shift_assignment()
        case "ASSIGNMENT_BITWISE_RIGHT_SHIFT":
            actions.user.code_operator_bitwise_right_shift_assignment()

        # code_operators_bitwise
        case "BITWISE_AND":
            actions.user.code_operator_bitwise_and()
        case "BITWISE_OR":
            actions.user.code_operator_bitwise_or()
        case "BITWISE_NOT":
            actions.user.code_operator_bitwise_not()
        case "BITWISE_EXCLUSIVE_OR":
            actions.user.code_operator_bitwise_exclusive_or()
        case "BITWISE_LEFT_SHIFT":
            actions.user.code_operator_bitwise_left_shift()
        case "BITWISE_RIGHT_SHIFT":
            actions.user.code_operator_bitwise_right_shift()

        # code_operators_lambda
        case "LAMBDA":
            actions.user.code_operator_lambda()

        # code_operators_math
        case "MATH_SUBTRACT":
            actions.user.code_operator_subtraction()
        case "MATH_ADD":
            actions.user.code_operator_addition()
        case "MATH_MULTIPLY":
            actions.user.code_operator_multiplication()
        case "MATH_DIVIDE":
            actions.user.code_operator_division()
        case "MATH_MODULO":
            actions.user.code_operator_modulo()
        case "MATH_EXPONENT":
            actions.user.code_operator_exponent()
        case "MATH_EQUAL":
            actions.user.code_operator_equal()
        case "MATH_NOT_EQUAL":
            actions.user.code_operator_not_equal()
        case "MATH_GREATER_THAN":
            actions.user.code_operator_greater_than()
        case "MATH_GREATER_THAN_OR_EQUAL":
            actions.user.code_operator_greater_than_or_equal_to()
        case "MATH_LESS_THAN":
            actions.user.code_operator_less_than()
        case "MATH_LESS_THAN_OR_EQUAL":
            actions.user.code_operator_less_than_or_equal_to()
        case "MATH_AND":
            actions.user.code_operator_and()
        case "MATH_OR":
            actions.user.code_operator_or()
        case "MATH_NOT":
            actions.user.code_operator_not()
        case "MATH_IN":
            actions.user.code_operator_in()
        case "MATH_NOT_IN":
            actions.user.code_operator_not_in()

        # code_operators_pointer
        case "POINTER_INDIRECTION":
            actions.user.code_operator_indirection()
        case "POINTER_ADDRESS_OF":
            actions.user.code_operator_address_of()
        case "POINTER_STRUCTURE_DEREFERENCE":
            actions.user.code_operator_structure_dereference()

        case _:
            raise ValueError(f"Operator {identifier} not found")
