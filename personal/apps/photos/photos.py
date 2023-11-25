from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.photos = """
os: mac
and app.bundle: com.apple.Photos
"""