from talon import Context, Module, actions

mod = Module()
apps = mod.apps
apps.obsidian = "app.name: Obsidian"

ctx = Context()
ctx.matches = r"""
app: obsidian
"""
ctx.tags = ["user.code_language_forced"]


@ctx.action_class("user")
class UserActions:
    def code_get_forced_language():
        return actions.user.code_get_forced_language_with_fallback("markdown")
