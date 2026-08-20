from talon import Context, Module, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: typst
"""

@ctx.action_class("user")
class UserActions:
    def code_comment_line_prefix():
        actions.insert("// ")

    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

    def code_insert_null():
        actions.insert("none")

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + f"({selection})"
        else:
            text = text + "()"
        actions.user.paste(text)
        actions.edit.left()
