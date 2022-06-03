from talon import Context, actions
ctx = Context()
ctx.matches = r"""
mode: user.c
mode: command
and code.language: c
"""

@ctx.action_class('user')
class UserActions:
    def code_operator_indirection():           actions.auto_insert('*')
    def code_operator_address_of():            actions.auto_insert('&')
    def code_operator_structure_dereference(): actions.auto_insert('->')
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
    #action(user.code_operator_exponent): " ** "
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
    def code_operator_and():                             actions.auto_insert(' && ')
    def code_operator_or():                              actions.auto_insert(' || ')
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
    def code_null():                                     actions.auto_insert('NULL')
    def code_is_null():                                  actions.auto_insert(' == NULL ')
    def code_is_not_null():                              actions.auto_insert(' != NULL')
    def code_state_if():
        actions.insert('if () {\n}\n')
        actions.key('up:2 left:3')
    def code_state_else_if():
        actions.insert('else if () {\n}\n')
        actions.key('up:2 left:3')
    def code_state_else():
        actions.insert('else\n{\n}\n')
        actions.key('up:2')
    def code_state_switch():
        actions.insert('switch ()')
        actions.edit.left()
    def code_state_case():
        actions.insert('case \nbreak;')
        actions.edit.up()
    def code_state_for():   actions.auto_insert('for ')
    def code_state_go_to(): actions.auto_insert('goto ')
    def code_state_while():
        actions.insert('while ()')
        actions.edit.left()
    def code_state_return():    actions.auto_insert('return ')
    def code_break():           actions.auto_insert('break;')
    def code_next():            actions.auto_insert('continue;')
    def code_true():            actions.auto_insert('true')
    def code_false():           actions.auto_insert('false')
    def code_type_definition(): actions.auto_insert('typedef ')
    def code_typedef_struct():
        actions.insert('typedef struct')
        actions.insert('{\n\n}')
        actions.edit.up()
        actions.key('tab')
    def code_from_import(): actions.auto_insert('using ')
    def code_include():     actions.insert('#include ')
    def code_include_system():
        actions.insert('#include <>')
        actions.edit.left()
    def code_include_local():
        actions.insert('#include ""')
        actions.edit.left()
    def code_comment(): actions.auto_insert('//')
    def code_block_comment():
        actions.insert('/*')
        actions.key('enter')
        actions.key('enter')
        actions.insert('*/')
        actions.edit.up()
    def code_block_comment_prefix(): actions.auto_insert('/*')
    def code_block_comment_suffix(): actions.auto_insert('*/')
