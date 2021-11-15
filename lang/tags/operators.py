from talon import Context, Module

ctx = Context()
mod = Module()

# TODO: rename this tag to 'code_operator' for consistency?
mod.tag("code_operators", desc="Tag for enabling generic operator commands")


@mod.action_class
class Actions:

    def code_operator_lambda():
        """code_operator_lambda"""

    def code_operator_subscript():
        """code_operator_subscript (e.g., C++ [])"""

    def code_operator_subtraction():
        """code_operator_subtraction"""

    def code_operator_addition():
        """code_operator_addition"""

    def code_operator_multiplication():
        """code_operator_multiplication"""

    def code_operator_exponent():
        """code_operator_exponent"""

    def code_operator_division():
        """code_operator_division"""

    def code_operator_modulo():
        """code_operator_modulo"""

    def code_operator_equal():
        """code_operator_equal"""

    def code_operator_not_equal():
        """code_operator_not_equal"""

    def code_operator_greater_than():
        """code_operator_greater_than"""

    def code_operator_greater_than_or_equal_to():
        """code_operator_greater_than_or_equal_to"""

    def code_operator_less_than():
        """code_operator_less_than"""

    def code_operator_less_than_or_equal_to():
        """code_operator_less_than_or_equal_to"""

    def code_operator_in():
        """code_operator_in"""

    def code_operator_and():
        """code_operator_and"""

    def code_operator_or():
        """code_operator_or"""

    def code_operator_bitwise_and():
        """code_operator_bitwise_and"""

    def code_operator_bitwise_or():
        """code_operator_bitwise_or"""

    def code_operator_bitwise_exclusive_or():
        """code_operator_bitwise_exclusive_or"""

    def code_operator_bitwise_left_shift():
        """code_operator_bitwise_left_shift"""

    def code_operator_bitwise_right_shift():
        """code_operator_bitwise_right_shift"""
