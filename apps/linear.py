from talon import ctrl, ui, Module, Context, actions, clip, app

ctx = Context()
mod = Module()
apps = mod.apps
apps.linear = """
app.name: Linear
"""
ctx.matches = r"""
app: linear
"""
