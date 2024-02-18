from talon import ui, Module, Context, registry, actions, imgui, cron

ctx_running = Context()
ctx_running.matches = r"""
os: windows
user.running: TechSmith Capture
"""
mod = Module()

mod.apps.tech_smith_capture = r"""
os: windows
and app.name: TechSmith Capture
os: windows
and app.exe: /^relayrecorder\.exe$/i
"""


@ctx_running.action_class("user")
class UserActionsWin:
    def screenshot_selection():
        actions.key("shift-f11")

    def screenshot_selection_clip():
        actions.key("shift-f11")