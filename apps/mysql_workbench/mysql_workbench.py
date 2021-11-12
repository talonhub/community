from talon import Context
ctx = Context()
ctx.matches = """
app.bundle: com.oracle.workbench.MySQLWorkbench
"""
@ctx.action_class("code")
class CodeActions:
    def language(): return "sql"