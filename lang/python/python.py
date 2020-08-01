from talon import Module, Context, actions, ui, imgui, clip

ctx = Context()
ctx.matches = r"""
mode: user.python
mode: command 
and code.language: python
"""
ctx.lists["user.code_functions"] = {
    "enumerate": "enumerate",
    "integer": "int",
    "length": "len",
    "list": "list",
    "print": "print",
    "range": "range",
    "set": "set",
    "split": "split",
    "string": "str",
    "update": "update",
}


@ctx.action_class("user")
class user_actions:
    def code_insert_function(text: str, selection: str):
        actions.clip.set_text(text + "({})".format(selection))
        actions.edit.paste()
        actions.edit.left()

