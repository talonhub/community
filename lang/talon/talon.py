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


@ctx.action_class("user")
class user_actions:
    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()
