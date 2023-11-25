from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.system_settings = """
os: mac
and app.bundle: com.apple.systempreferences
"""