from talon import Context, Module, actions, imgui, registry, settings

ctx = Context()
mod = Module()

mod.list("code_common_function", desc="List of common functions for active language")

# global
function_list = []

@mod.capture(rule="{user.code_common_function}")
def code_common_function(m) -> str:
    """Returns a function name"""
    return m.code_common_function

mod.tag("code_functions_common", desc="Tag for enabling support for common functions")
mod.tag("code_functions_common_gui_active", desc="Active when the function picker GUI is showing")

@mod.action_class
class Actions:

    def code_toggle_functions():
        """GUI: List functions for active language"""
        global function_list
        if gui_functions.showing:
            function_list = []
            gui_functions.hide()
            ctx.tags.discard("user.code_functions_common_gui_active")
        else:
            update_function_list_and_freeze()

    def code_select_function(number: int, selection: str):
        """Inserts the selected function when the imgui is open"""
        if gui_functions.showing and number < len(function_list):
            actions.user.code_insert_function(
                registry.lists["user.code_common_function"][0][function_list[number]],
                selection,
            )

    # TODO: clarify the relation between `code_insert_function`
    #       and the various functions declared in the functions

    def code_insert_function(text: str, selection: str):
        """Inserts a function and positions the cursor appropriately"""


def update_function_list_and_freeze():
    global function_list
    if "user.code_common_function" in registry.lists:
        function_list = sorted(registry.lists["user.code_common_function"][0].keys())
    else:
        function_list = []

    gui_functions.show()
    ctx.tags.add("user.code_functions_common_gui_active")


@imgui.open()
def gui_functions(gui: imgui.GUI):
    gui.text("Functions")
    gui.line()

    # print(str(registry.lists["user.code_functions"]))
    for i, entry in enumerate(function_list, 1):
        if entry in registry.lists["user.code_common_function"][0]:
            gui.text(
                "{}. {}: {}".format(
                    i, entry, registry.lists["user.code_common_function"][0][entry]
                )
            )

    gui.spacer()
    if gui.button("Toggle funk (close window)"):
        actions.user.code_toggle_functions_hide()


def commands_updated(_):
    if gui_functions.showing:
        update_function_list_and_freeze()


registry.register("update_commands", commands_updated)
