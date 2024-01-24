from talon import Module, ui

mod = Module()


@mod.scope
def scope():
    return {"running": {app.name.lower() for app in ui.apps()}}


ui.register("app_launch", scope.update)
ui.register("app_close", scope.update)
