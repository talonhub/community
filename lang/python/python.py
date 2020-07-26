from talon import Module, Context, actions, ui, imgui, clip

ctx = Context()
ctx.matches = r"""
mode: user.python
mode: command 
and code.language: python
"""
ctx.lists["user.code_functions"] = {
    "print": "print",
    "length": "len",
    "string": "str",
    "integer": "int",
    "enumerate": "enumerate",
    "update": "update",
    "split": "split",
    "set": "set",
    "list": "list",
    "range": "range",
}


@ctx.action_class("user")
class user_actions:
    def code_insert_function(text: str, selection: str):
        actions.clip.set_text(text + "({})".format(selection))
        actions.edit.paste()
        actions.edit.left()

