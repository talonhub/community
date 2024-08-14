from talon import Context, Module

mod = Module()
mod.apps.obsidian = "app.name: Obsidian"

lang_ctx = Context()
lang_ctx.matches = r"""
app: obsidian
not tag: user.code_language_forced
"""


@lang_ctx.action_class("code")
class CodeActions:
    def language():
        return "markdown"
