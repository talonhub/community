from talon import Module, Context, actions, ui, imgui

ctx = Context()
ctx.matches = r"""
mode: user.csharp
mode: command 
and code.language: csharp
"""
ctx.lists["user.code_functions"] = {
    "print": "Console.WriteLine",
    "string": ".ToString",
    "integer": "int.TryParse",
}


@ctx.action_class("user")
class user_actions:
    def code_insert_function(text: str):
        actions.insert(text + "()")
        actions.edit.left()
