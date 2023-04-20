from talon import ui, Module, Context, registry, actions, imgui, cron

mod = Module()

mod.apps.tech_smith_capture = """
os: windows
and app.name: TechSmith Capture
os: windows
and app.exe: RelayRecorder.exe
"""