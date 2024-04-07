from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.microsoft_word = r"""
os: windows
and app.exe: /^chrome\.exe$/i
win.title: /\.docx/
win.title: /\.doc/
"""
mod.apps.microsoft_word = r"""
os: windows
and app.name: Microsoft Edge
os: windows
and app.exe: /^msedge\.exe$/i
win.title: /\.docx/
win.title: /\.doc/
"""

# @mod.action_class
# class Actions:
