# this functionality is only available in the talon beta
from talon import Module

mod = Module()
mod.apps.talon_debug_window = """
os: mac
and app.bundle: com.talonvoice.Talon
win.title: Talon Debug
"""
mod.apps.talon_debug_window = """
os: windows
and app.name: Talon
os: windows
and app.exe: talon.exe
win.title: Talon Debug
"""
