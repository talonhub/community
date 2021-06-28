from talon import Context, actions
ctx = Context()
ctx.matches = r"""
mode: user.vimscript
mode: command
and code.language: vimscript
"""

@ctx.action_class('user')
class UserActions:
    def code_operator_assignment():                actions.auto_insert(' = ')
    def code_operator_subtraction():               actions.auto_insert(' - ')
    def code_operator_subtraction_assignment():    actions.auto_insert(' -= ')
    def code_operator_addition():                  actions.auto_insert(' + ')
    def code_operator_addition_assignment():       actions.auto_insert(' += ')
    def code_operator_multiplication():            actions.auto_insert(' * ')
    def code_operator_multiplication_assignment(): actions.auto_insert(' *= ')
    def code_operator_division():                  actions.auto_insert(' / ')
    def code_operator_division_assignment():       actions.auto_insert(' /= ')
    
    # comments - see lang/code_comment.talon
    def code_comment():                            actions.auto_insert('"')
    
    # conditionals - see lang/programming.talon
    def code_state_if():
        actions.insert('if ')
    def code_state_else_if():
        actions.insert('elseif ')
    def code_state_else():
        actions.insert('else')
    def code_private_function(text: str):   actions.auto_insert('function ')
    def code_protected_function(text: str): actions.auto_insert('function ')
    def code_public_function(text: str):    actions.auto_insert('function ')
