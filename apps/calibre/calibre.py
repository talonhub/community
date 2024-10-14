from talon import Module

# --- App definition ---
mod = Module()
mod.apps.calibre = r"""
os: windows
and app.name: calibre.exe
os: windows
and app.exe: /^calibre\.exe$/i
os: windows
and app.name: calibre-parallel.exe
os: windows
and app.exe: /^calibre-parallel\.exe$/i
"""
mod.apps.calibre = """
os: linux
app.name: calibre
"""
# TODO: mac context
