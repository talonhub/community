from talon import Context, actions
ctx = Context()
ctx.matches = r"""
mode: user.r
mode: command
and code.language: r
"""

@ctx.action_class('user')
class UserActions:
    def code_operator_assignment():               actions.auto_insert(' <- ')
    def code_operator_subtraction():              actions.auto_insert(' - ')
    def code_operator_addition():                 actions.auto_insert(' + ')
    def code_operator_multiplication():           actions.auto_insert(' * ')
    def code_operator_exponent():                 actions.auto_insert(' ** ')
    def code_operator_division():                 actions.auto_insert(' / ')
    def code_operator_modulo():                   actions.auto_insert(' %% ')
    def code_operator_equal():                    actions.auto_insert(' == ')
    def code_operator_not_equal():                actions.auto_insert(' != ')
    def code_operator_greater_than():             actions.auto_insert(' > ')
    def code_operator_greater_than_or_equal_to(): actions.auto_insert(' >= ')
    def code_operator_less_than():                actions.auto_insert(' < ')
    def code_operator_less_than_or_equal_to():    actions.auto_insert(' <= ')
    def code_operator_in():                       actions.auto_insert(' %in% ')
    def code_operator_and():                      actions.auto_insert(' & ')
    def code_operator_or():                       actions.auto_insert(' | ')
    def code_operator_bitwise_and():              actions.auto_insert(' & ')
    def code_null():                              actions.auto_insert('NULL')
    def code_state_if():
        actions.insert('if () {}')
        actions.key('left enter up end left:3')
    def code_state_else_if():
        actions.insert(' else if () {}')
        actions.key('left enter up end left:3')
    def code_state_else():
        actions.insert(' else {}')
        actions.key('left enter')
    def code_state_for():
        actions.insert('for ( in ) {}')
        actions.key('left enter up end left:7')
    def code_state_while():
        actions.insert('while () {}')
        actions.key('left enter up end left:3')
    def code_import():
        actions.insert('library()')
        actions.key('left')
    def code_comment(): actions.auto_insert('#')
    def code_state_return():
        actions.insert('return()')
        actions.key('left')
    def code_break(): actions.auto_insert('break')
    def code_next():  actions.auto_insert('next')
    def code_true():  actions.auto_insert('TRUE')
    def code_false(): actions.auto_insert('FALSE')
