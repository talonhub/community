from talon import Context, actions
ctx = Context()
ctx.matches = r"""
mode: user.java
mode: command
and code.language: java
"""
ctx.tags = ['user.code_operators', 'user.code_generic']

@ctx.action_class('user')
class UserActions:
    def code_operator_indirection(): actions.skip()
    def code_operator_address_of(): actions.skip()
    def code_operator_lambda(): actions.auto_insert(' -> ')
    def code_operator_subscript():
        actions.insert('[]')
        actions.key('left')
    def code_operator_assignment(): actions.auto_insert(' = ')
    def code_operator_subtraction(): actions.auto_insert(' - ')
    def code_operator_subtraction_assignment(): actions.auto_insert(' -= ')
    def code_operator_addition(): actions.auto_insert(' + ')
    def code_operator_addition_assignment(): actions.auto_insert(' += ')
    def code_operator_multiplication(): actions.auto_insert(' * ')
    def code_operator_multiplication_assignment(): actions.auto_insert(' *= ')
    def code_operator_exponent(): actions.auto_insert(' ^ ')
    def code_operator_division(): actions.auto_insert(' / ')
    def code_operator_division_assignment(): actions.auto_insert(' /= ')
    def code_operator_modulo(): actions.auto_insert(' % ')
    def code_operator_modulo_assignment(): actions.auto_insert(' %= ')
    def code_operator_equal(): actions.auto_insert(' == ')
    def code_operator_not_equal(): actions.auto_insert(' != ')
    def code_operator_greater_than(): actions.auto_insert(' > ')
    def code_operator_greater_than_or_equal_to(): actions.auto_insert(' >= ')
    def code_operator_less_than(): actions.auto_insert(' < ')
    def code_operator_less_than_or_equal_to(): actions.auto_insert(' <= ')
    def code_operator_and(): actions.auto_insert(' && ')
    def code_operator_or(): actions.auto_insert(' || ')
    def code_operator_bitwise_and(): actions.auto_insert(' & ')
    def code_operator_bitwise_or(): actions.auto_insert(' | ')
    def code_operator_bitwise_exclusive_or(): actions.auto_insert(' ^ ')
    def code_operator_bitwise_left_shift(): actions.auto_insert(' << ')
    def code_operator_bitwise_left_shift_assignment(): actions.auto_insert(' <<= ')
    def code_operator_bitwise_right_shift(): actions.auto_insert(' >> ')
    def code_operator_bitwise_right_shift_assignment(): actions.auto_insert(' >>= ')
    def code_self(): actions.auto_insert('this')
    def code_null(): actions.auto_insert('null')
    def code_is_null(): actions.auto_insert(' == null')
    def code_is_not_null(): actions.auto_insert(' != null')
    def code_state_if():
        actions.insert('if () ')
        actions.key('left')
        actions.key('left')
    def code_state_else_if():
        actions.insert('else if () ')
        actions.key('left')
        actions.key('left')
    def code_state_else():
        actions.insert('else ')
        actions.key('enter')
    def code_state_switch():
        actions.insert('switch () ')
        actions.key('left')
        actions.edit.left()
    def code_state_case():
        actions.insert('case \nbreak;')
        actions.edit.up()
    def code_state_for():
        actions.insert('for () ')
        actions.key('left')
        actions.key('left')
    def code_state_while():
        actions.insert('while () ')
        actions.edit.left()
        actions.edit.left()
    def code_type_class(): actions.auto_insert('class ')
    def code_private_function(text: str):
        actions.insert('private')
    def code_protected_function(text: str):
        actions.user.code_private_function()
    def code_public_function(text: str):
        actions.insert('public ')
    def code_state_return():
        actions.insert('return ')
