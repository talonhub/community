from talon import Module, Context, actions
from ...core.imgui import imgui

mod = Module()
ctx = Context()

mod.tag("help_running_apps", "Help running applications gui is showing")


@imgui.open(numbered=True)
def gui(gui: imgui.GUI):
    gui.header("Running apps")
    gui.line(bold=True)
    for name in actions.user.get_running_applications():
        gui.text(name)
    gui.spacer()
    if gui.button("Hide"):
        actions.user.help_running_apps_toggle()


@mod.action_class
class Actions:
    def help_running_apps_toggle():
        """Toggle running applications help gui"""
        if gui.showing:
            actions.user.help_running_apps_hide()
        else:
            ctx.tags = ["self.help_running_apps"]
            gui.show()

    def help_running_apps_hide():
        """Hide running applications help gui"""
        ctx.tags = []
        gui.hide()
