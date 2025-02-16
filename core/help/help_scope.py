from talon import Context, Module, actions, imgui, scope, settings, ui, app
from ...core.app_switcher.windows import get_application_user_model_id, get_application_user_model_for_window

ctx = Context()
mod = Module()
mod.tag("help_scope_open", "tag for showing the scope help gui")

mod.setting(
    "help_scope_max_length",
    type=int,
    default=50,
)


@imgui.open(x=ui.main_screen().x)
def gui(gui: imgui.GUI):
    gui.text("Scope")
    gui.line()
    gui.spacer()
    gui.text("Modes")
    gui.line()
    for mode in sorted(scope.get("mode")):
        gui.text(mode)
    gui.spacer()
    gui.text("Tags")
    gui.line()
    for tag in sorted(scope.get("tag")):
        gui.text(tag)
    gui.spacer()
    gui.text("Misc")
    gui.line()
    ignore = {"main", "mode", "tag"}
    keys = {*scope.data.keys(), *scope.data["main"].keys()}
    for key in sorted(keys):
        if key not in ignore:
            value = scope.get(key)
            print_value(gui, key, value, ignore)
    gui.spacer()
    # if app.platform=="windows":
    #     gui.text("Windows-specific")
    #     application_user_model_id = None
    #     window_application_user_model_id = None
    #     try:
    #         application_user_model_id = get_application_user_model_id(ui.active_app().pid)
    #     except:
    #         pass
    #     try:
    #         window_application_user_model_id = get_application_user_model_id(ui.active_app().pid)
    #     except:
    #         pass

    #     gui.text(f"AppUserModelId: {application_user_model_id}")
    #     gui.text(f"Window AppUserModelId: {window_application_user_model_id}")
    #     gui.text(f"Window cls: {ui.active_window().cls}")
    if gui.button("Hide"):
        actions.user.help_scope_toggle()


def print_value(gui: imgui.GUI, path: str, value, ignore: set[str] = {}):
    if isinstance(value, dict):
        for key in value:
            if key not in ignore:
                p = f"{path}.{key}" if path else key
                print_value(gui, p, value[key])
    elif value:
        gui.text(f"{path}: {format_value(value)}")


def format_value(value):
    if isinstance(value, (list, set)):
        value = ", ".join(sorted(value))
    setting_max_length = settings.get("user.help_scope_max_length")
    if isinstance(value, str) and len(value) > setting_max_length + 4:
        return f"{value[:setting_max_length]} ..."
    return value


@mod.action_class
class Actions:
    def help_scope_toggle():
        """Toggle help scope gui"""
        if gui.showing:
            ctx.tags = []
            gui.hide()
        else:
            ctx.tags = ["user.help_scope_open"]
            gui.show()
