from talon import ui, Module, Context, registry, actions, imgui, cron

mod = Module()
mod.apps.screen_clipping_host = """
os: windows
and app.name: ScreenClippingHost.exe
os: windows
and app.exe: ScreenClippingHost.exe
"""
