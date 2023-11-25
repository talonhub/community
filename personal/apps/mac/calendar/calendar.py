from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.calendar = """
os: mac
and app.bundle: com.apple.iCal
"""