from talon import ctrl, ui, Module, Context, actions, clip, app

ctx = Context()
mod = Module()

mod.apps.brave = "app.name: Brave"

ctx.matches = r"""
app: brave
"""
