from talon import Module, Context, actions, ui, imgui, clip, settings

ctx = Context()
ctx.matches = r"""
mode: user.talon
mode: command 
and code.language: talon
"""
ctx.lists["user.code_functions"] = {
    "insert": "insert",
    "key": "key",
    "print": "print",
    "repeat": "repeat",
}


@ctx.action_class('user')
class UserActions:
    def code_operator_and():            actions.auto_insert(' and ')
    def code_operator_or():             actions.auto_insert(' or ')
    def code_operator_subtraction():    actions.auto_insert(' - ')
    def code_operator_addition():       actions.auto_insert(' + ')
    def code_operator_multiplication(): actions.auto_insert(' * ')
    def code_operator_division():       actions.auto_insert(' / ')
    def code_operator_assignment():     actions.auto_insert(' = ')
    def code_comment():                 actions.auto_insert('#')
    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()
