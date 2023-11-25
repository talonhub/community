from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.podcasts = """
os: mac
and app.bundle: com.apple.podcasts
"""