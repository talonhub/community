from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.keynote = """
os: mac
and app.bundle: com.apple.iWork.Keynote
"""