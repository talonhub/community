from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.reminders = """
os: mac
and app.bundle: com.apple.reminders
"""