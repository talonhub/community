from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_operators_assignment", desc="Tag for enabling assignment commands")


@mod.action_class
class Actions:
    def code_operator_assignment():
        """code_operator_assignment"""

    def code_operator_subtraction_assignment():
        """code_operator_subtraction_equals"""

    def code_operator_addition_assignment():
        """code_operator_addition_assignment"""

    def code_operator_increment():
        """code_operator_increment"""

    def code_operator_multiplication_assignment():
        """code_operator_multiplication_assignment"""

    def code_operator_division_assignment():
        """code_operator_division_assignment"""

    def code_operator_modulo_assignment():
        """code_operator_modulo_assignment"""

    def code_operator_bitwise_and_assignment():
        """code_operator_and"""

    def code_operator_bitwise_or_assignment():
        """code_operator_or_assignment"""

    def code_operator_bitwise_exclusive_or_assignment():
        """code_operator_bitwise_exclusive_or_assignment"""

    def code_operator_bitwise_left_shift_assignment():
        """code_operator_bitwise_left_shift_assigment"""

    def code_operator_bitwise_right_shift_assignment():
        """code_operator_bitwise_right_shift_assignment"""
