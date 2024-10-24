from talon import Context, Module

mod = Module()
mod.apps.talon_repl = r"""
win.title: /Talon - REPL/
win.title: /Users/knausj/.talon/.venv/bin/repl
"""

ctx = Context()
ctx.matches = r"""
app: talon_repl
not tag: user.code_language_forced
"""


@ctx.action_class("code")
class CodeActions:
    def language():
        return "python"
