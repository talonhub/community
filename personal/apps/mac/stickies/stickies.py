from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.stickies = """
os: mac
and app.bundle: com.apple.Stickies
"""