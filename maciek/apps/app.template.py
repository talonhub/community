from talon import Context, actions, ui, Module, app, clip

mod = Module()

mod.apps.kitty = """
app.name: kitty
"""

mod.apps.kitty = """
os: mac
and app.bundle: net.kovidgoyal.kitty
"""

ctx = Context()
ctx.matches = r"""
app: kitty
"""
