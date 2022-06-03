from talon import Context, actions
ctx = Context()
ctx.matches = r"""
mode: user.talon
mode: command
and code.language: talon
"""

@ctx.action_class('user')
class UserActions:
    def code_operator_and():            actions.auto_insert(' and ')
    def code_operator_or():             actions.auto_insert(' or ')
    def code_operator_subtraction():    actions.auto_insert(' - ')
    def code_operator_addition():       actions.auto_insert(' + ')
    def code_operator_multiplication(): actions.auto_insert(' * ')
    def code_operator_division():       actions.auto_insert(' / ')
    def code_operator_assignment():     actions.auto_insert(' = ')
    def code_comment():                 actions.auto_insert('# ')
