from talon import Module, Context, actions, ui, imgui, clip

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
        actions.clip.set_text(text + "({})".format(selection))
        actions.edit.paste()
        actions.edit.left()

