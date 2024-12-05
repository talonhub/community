from talon import Module, ui

mod = Module()

# List of running applications
running_applications = {}

@mod.scope
def scope():
    return {"running": running_applications}

def update_running(_):
    global running_applications
    running_applications = {app.name.lower() for app in ui.apps(background = False)}
    scope.update()

@mod.action_class
class Actions:
    def get_running_applications() -> dict[str, str]:
        """Fetch a dict of running applications"""
        return running_applications


ui.register("app_launch", update_running)
ui.register("app_close", update_running)

