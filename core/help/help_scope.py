from typing import Optional

import egui
from talon import Context, Module, actions, scope, settings

from ..gui.gui import open_gui

ctx = Context()
mod = Module()
mod.tag("help_scope_open", "tag for showing the scope help gui")

mod.setting(
    "help_scope_max_length",
    type=int,
    default=50,
)


@open_gui(x=0, y=0, refresh_period="100ms")
async def gui(ui, ui_wrapper):
    ui_wrapper.title("Scope")
    ui_wrapper.spacing()
    ui.strong("Modes")
    ui.separator()
    for mode in sorted(scope.get("mode")):
        ui.label(mode)
    ui_wrapper.spacing()
    ui.strong("Tags")
    ui.separator()
    for tag in sorted(scope.get("tag")):
        ui.label(tag)
    ui_wrapper.spacing()
    ui.strong("Misc")
    ui.separator()
    ignore = {"main", "mode", "tag"}
    keys = {*scope.data.keys(), *scope.data["main"].keys()}
    for key in sorted(keys):
        if key not in ignore:
            value = scope.get(key)
            render_value(ui, key, value, ignore)
    ui_wrapper.spacing()
    if ui_wrapper.command_button("scope close"):
        actions.user.help_scope_toggle()
    
    # if we update this to use a scroll area or table, we will want to only call this when the
    # width of the gui changes
    gui.auto_size_next_frame()


def render_value(ui: egui.Ui, path: str, value, ignore: Optional[set[str]] = None):
    if isinstance(value, dict):
        if not ignore:
            ignore = set()
        for key in value:
            if key not in ignore:
                p = f"{path}.{key}" if path else key
                render_value(ui, p, value[key])
    elif value:
        ui.label(f"{path}: {format_value(value)}")


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
