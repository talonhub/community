from talon import Module

mod = Module()
mod.apps.talon_debug = """
os: mac
and app.bundle: com.talonvoice.Talon
win.title: Talon Debug
"""
mod.apps.talon_debug = """
os: windows
and app.name: Talon
os: windows
and app.exe: talon.exe   
"""
