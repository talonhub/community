from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.music = """
os: mac
and app.bundle: com.apple.Music
"""