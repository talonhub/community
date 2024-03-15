from talon import Context

ctx = Context()
ctx.matches = r"""
app: stata
"""

@ctx.action_class("code")
class CodeActions:
    def language():
        return "stata"
    

        