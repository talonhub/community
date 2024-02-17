from talon import Module

# --- App definition ---
mod = Module()
mod.apps.adobe_acrobat_reader_dc = r"""
os: windows
and app.name: Adobe Acrobat DC
os: windows
and app.exe: /^acrobat\.exe$/i
os: windows
and app.name: Adobe Acrobat Reader DC
os: windows
and app.exe: /^acrord32\.exe$/i
"""
# TODO: mac context and implementation
