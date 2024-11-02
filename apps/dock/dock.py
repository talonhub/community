from talon import Context, Module, actions, clip, ui

ctx = Context()
mod = Module()

ctx.matches = """
os: mac
"""


@mod.action_class
class Actions:
    def dock_send_notification(notification: str):
        """Send a CoreDock notification to the macOS Dock using SPI"""


@ctx.action_class("user")
class UserActions:
    def dock_send_notification(notification: str):
        from talon.mac.dock import dock_notify

        dock_notify(notification)
