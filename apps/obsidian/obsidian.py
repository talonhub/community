from talon import Context, Module

mod = Module()
apps = mod.apps
apps.obsidian = "app.name: Obsidian"

ctx = Context()
ctx.matches = r"""
app: obsidian
"""

lang_ctx = Context()
lang_ctx.matches = r"""
app: obsidian
not tag: user.code_language_forced
"""


@lang_ctx.action_class("code")
class CodeActions:
    def language():
        return "markdown"
