from talon import Module

mod = Module()
apps = mod.apps
apps.opera = "app.name: Opera"
apps.opera = "app.name: Opera Internet Browser"
apps.opera = """
os: mac
and app.bundle: com.operasoftware.Opera
"""
apps.opera = r"""
os: windows
and app.exe: /^opera\.exe$/i
"""
apps.opera = """
os: linux
and app.exe: opera
"""
