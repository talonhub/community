from talon import Context, Module

mod = Module()
ctx = Context()

mod.apps.stata = r"""
os: windows
and app.name: Stata
os: windows
and app.exe: /^statase\-64\.exe$/i
"""

ctx.matches = r"""
app: stata
"""


@ctx.action_class("code")
class CodeActions:
    def language():
        return "stata"
