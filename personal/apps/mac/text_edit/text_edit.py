from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.text_edit = """
os: mac
and app.bundle: com.apple.TextEdit
"""