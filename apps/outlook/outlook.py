from talon import Module 
mod = Module()
mod.apps.microsoft_outlook = r"""
os: windows
and app.name: Microsoft Outlook
os: windows
and app.exe: /^olk\.exe$/i
"""