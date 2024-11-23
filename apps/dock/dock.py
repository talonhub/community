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

    def dock_app_expose():
        """Activate app Exposé using the macOS Dock item for the frontmost app"""


@ctx.action_class("user")
class UserActions:
    def dock_app_expose(app: Optional[App]):
        if app is None:
            app = ui.active_app()

        app_name = Path(ui.active_app().path).stem
        dock_items = ui.apps(bundle="com.apple.dock")[0].children.find(
            AXSubrole="AXApplicationDockItem", AXTitle=app_name, max_depth=1
        )
        match len(dock_items):
            case 1:
                dock_items[0].perform("AXShowExpose")
            case 0:
                actions.app.notify(
                    body=f"No dock icon for “{app_name}”",
                    title="Unable to activate App Exposé",
                )
            case _:
                actions.app.notify(
                    body=f"Multiple dock icons for “{app_name}”",
                    title="Unable to activate App Exposé",
                )

    def dock_send_notification(notification: str):
        from talon.mac.dock import dock_notify

        dock_notify(notification)
