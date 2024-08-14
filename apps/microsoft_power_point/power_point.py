from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.microsoft_power_point = r"""
os: windows
and app.name: Microsoft PowerPoint
os: windows
and app.exe: /^powerpnt\.exe$/i
"""

# @mod.action_class
# class Actions:
