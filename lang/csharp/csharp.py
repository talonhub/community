from talon import Module, Context, actions, ui, imgui

ctx = Context()
ctx.matches = r"""
mode: user.csharp
mode: command 
and code.language: csharp
"""
ctx.lists["user.code_functions"] = {
    "integer": "int.TryParse",
    "print": "Console.WriteLine",
    "string": ".ToString",
}


@ctx.action_class("user")
class user_actions:
    def code_insert_function(text: str, selection: str):
        actions.clip.set_text(text + "({})".format(selection))
        actions.edit.paste()
        actions.edit.left()
