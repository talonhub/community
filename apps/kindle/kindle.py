from talon import Module

# --- App definition ---
mod = Module()
mod.apps.kindle = """
os: windows
and app.name: Kindle
os: windows
and app.exe: Kindle.exe
"""
# TODO: mac context and implementation
