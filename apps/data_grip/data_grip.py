from talon import Context
ctx = Context()
ctx.matches = """
app: datagrip
"""
@ctx.action_class("code")
class CodeActions:
    def language(): return "sql"