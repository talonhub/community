from talon import ctrl, ui, Module, Context, actions, clip, app

ctx = Context()
mod = Module()
apps = mod.apps
apps.preview = """
app.name: Preview
"""
ctx.matches = r"""
app: preview
"""
