# defines placeholder actions and captures for ide-specific snippet functionality
from talon import Module, actions, app, Context, imgui, registry

mod = Module()
ctx = Context()
mod.tag("snippets", desc="Tag for enabling code snippet-related commands")
mod.list("snippets", desc="List of code snippets")


@mod.capture
def snippets(m) -> list:
    """Returns a snippet name"""


@ctx.capture(rule="{user.snippets}")
def snippets(m):
    return m.snippets


@imgui.open(software=False)
def gui(gui: imgui.GUI):
    gui.text("snippets")
    gui.line()

    function_list = sorted(registry.lists["user.snippets"][0].keys())

    # print(str(registry.lists["user.code_functions"]))
    for i, entry in enumerate(function_list):
        gui.text("{}".format(entry, function_list))


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
        else:
            gui.show()

