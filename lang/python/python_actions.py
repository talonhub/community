from talon import Context, actions
ctx = Context()
ctx.matches = r"""
mode: user.python
mode: command
and code.language: python
"""

@ctx.action_class('user')
class UserActions:
    def code_operator_indirection():           actions.auto_insert('')
    def code_operator_address_of():            actions.auto_insert('')
    def code_operator_structure_dereference(): actions.auto_insert('')
    def code_operator_lambda():                actions.auto_insert('')
    def code_operator_subscript():
        actions.insert('[]')
        actions.key('left')
    def code_operator_assignment():                      actions.auto_insert(' = ')
    def code_operator_subtraction():                     actions.auto_insert(' - ')
    def code_operator_subtraction_assignment():          actions.auto_insert(' -= ')
    def code_operator_addition():                        actions.auto_insert(' + ')
    def code_operator_addition_assignment():             actions.auto_insert(' += ')
    def code_operator_multiplication():                  actions.auto_insert(' * ')
    def code_operator_multiplication_assignment():       actions.auto_insert(' *= ')
    def code_operator_exponent():                        actions.auto_insert(' ** ')
    def code_operator_division():                        actions.auto_insert(' / ')
    def code_operator_division_assignment():             actions.auto_insert(' /= ')
    def code_operator_modulo():                          actions.auto_insert(' % ')
    def code_operator_modulo_assignment():               actions.auto_insert(' %= ')
    def code_operator_equal():                           actions.auto_insert(' == ')
    def code_operator_not_equal():                       actions.auto_insert(' != ')
    def code_operator_greater_than():                    actions.auto_insert(' > ')
    def code_operator_greater_than_or_equal_to():        actions.auto_insert(' >= ')
    def code_operator_less_than():                       actions.auto_insert(' < ')
    def code_operator_less_than_or_equal_to():           actions.auto_insert(' <= ')
    def code_operator_and():                             actions.auto_insert(' and ')
    def code_operator_or():                              actions.auto_insert(' or ')
    def code_operator_bitwise_and():                     actions.auto_insert(' & ')
    def code_operator_bitwise_and_assignment():          actions.auto_insert(' &= ')
    def code_operator_bitwise_or():                      actions.auto_insert(' | ')
    def code_operator_bitwise_or_assignment():           actions.auto_insert(' |= ')
    def code_operator_bitwise_exclusive_or():            actions.auto_insert(' ^ ')
    def code_operator_bitwise_exclusive_or_assignment(): actions.auto_insert(' ^= ')
    def code_operator_bitwise_left_shift():              actions.auto_insert(' << ')
    def code_operator_bitwise_left_shift_assignment():   actions.auto_insert(' <<= ')
    def code_operator_bitwise_right_shift():             actions.auto_insert(' >> ')
    def code_operator_bitwise_right_shift_assignment():  actions.auto_insert(' >>= ')
    def code_self():                                     actions.auto_insert('self')
    def code_null():                                     actions.auto_insert('None')
    def code_is_null():                                  actions.auto_insert(' is None')
    def code_is_not_null():                              actions.auto_insert(' is not None')
    def code_state_if():
        actions.insert('if :')
        actions.key('left')
    def code_state_else_if():
        actions.insert('elif :')
        actions.key('left')
    def code_state_else():
        actions.insert('else:')
        actions.key('enter')
    def code_state_switch():
        actions.insert('switch ()')
        actions.edit.left()
    def code_state_case():
        actions.insert('case \nbreak;')
        actions.edit.up()
    def code_state_for(): actions.auto_insert('for ')
    def code_state_for_each():
        actions.insert('for in ')
        actions.key('left')
        actions.edit.word_left()
        actions.key('space')
        actions.edit.left()
    def code_state_while():
        actions.insert('while :')
        actions.edit.left()
    def code_type_class(): actions.auto_insert('class ')
    def code_import():     actions.auto_insert('import ')
    def code_from_import():
        actions.insert('from import ')
        actions.key('left')
        actions.edit.word_left()
        actions.key('space')
        actions.edit.left()
    def code_comment(): actions.auto_insert('# ')
    def code_state_return():
        actions.insert('return ')
    def code_true():            actions.auto_insert('True')
    def code_false():           actions.auto_insert('False')
    def code_document_string(): actions.user.insert_cursor('"""[|]"""')
