from talon import Context, Module

mod = Module()
ctx = Context()

mod.apps.positron = r"""
os: mac
and app.bundle: co.posit.positron
"""

ctx.matches = r"""
os: mac
app: positron
"""
