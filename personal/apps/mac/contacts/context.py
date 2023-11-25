from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.contacts = """
os: mac
and app.bundle: com.apple.AddressBook
"""