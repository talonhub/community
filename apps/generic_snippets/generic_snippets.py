# defines placeholder actions and captures for ide-specific snippet functionality
from talon import Module, actions, app, Context, imgui, registry

mod = Module()
mod.tag("snippets", desc="Tag for enabling code snippet-related commands")
mod.tag("snippets_showing", desc="Active when snippets UI is showing")
mod.list("snippets", desc="List of code snippets")
ctx = Context()


@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("snippets")
    gui.line()

    if "user.snippets" in registry.lists:
        function_list = sorted(registry.lists["user.snippets"][0].keys())
        # print(str(registry.lists["user.snippets"]))

        # print(str(registry.lists["user.code_functions"]))
        if function_list:
            for i, entry in enumerate(function_list):
                gui.text("{}".format(entry, function_list))

    gui.spacer()
    if gui.button("Snip close"):
        actions.user.snippet_hide()


@mod.action_class
class Actions:
    def snippet_search(text: str):
        """Triggers the program's snippet search"""

    def snippet_insert(text: str):
        """Inserts a snippet"""

    def snippet_create():
        """Triggers snippet creation"""

    def snippet_toggle():
        """Toggles UI for available snippets"""
        if gui.showing:
            gui.hide()
            ctx.tags = []
        else:
            gui.show()
            ctx.tags = ["user.snippets_showing"]

    def snippet_hide():
        """Hides the snippet UI"""
        gui.hide()
        ctx.tags = []
