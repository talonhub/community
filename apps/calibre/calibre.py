from talon import Module

# --- App definition ---
mod = Module()
mod.apps.calibre = """
os: windows
and app.name: calibre.exe
os: windows
and app.exe: calibre.exe
os: windows
and app.name: calibre-parallel.exe
os: windows
and app.exe: calibre-parallel.exe
"""
mod.apps.calibre = """
os: linux
app.name: calibre
"""
# TODO: mac context
