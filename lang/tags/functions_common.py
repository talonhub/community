from talon import Context, Module, actions, registry

from ...core.gui.gui import open_gui 

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
mod.tag(
    "code_functions_common_gui_active",
    desc="Active when the function picker GUI is showing",
)


@mod.action_class
class Actions:
    def code_toggle_functions():
        """GUI: List functions for active language"""
        global function_list
        if gui_functions.showing:
            function_list = []
            gui_functions.hide()
            ctx.tags = []
        else:
            update_function_list()

    def code_select_function(number: int, selection: str):
        """Inserts the selected function when the gui is open"""
        if gui_functions.showing and number < len(function_list):
            talon_list = actions.user.talon_get_active_registry_list(
                "user.code_common_function"
            )
            actions.user.code_insert_function(
                talon_list[function_list[number]],
                selection,
            )

    def code_insert_function(text: str, selection: str):
        """Inserts a function and positions the cursor appropriately"""


def update_function_list():
    global function_list
    if "user.code_common_function" in registry.lists:
        talon_list = actions.user.talon_get_active_registry_list(
            "user.code_common_function"
        )
        function_list = sorted(talon_list.keys())
    else:
        function_list = []

    gui_functions.auto_size_next_frame()
    if gui_functions.showing:
        gui_functions.refresh()
    gui_functions.show()
    ctx.tags = ["user.code_functions_common_gui_active"]


@open_gui()
async def gui_functions(ui, ui_wrapper):
    ui_wrapper.title("Functions")

    for i, entry in enumerate(function_list, 1):
        talon_list = actions.user.talon_get_active_registry_list(
            "user.code_common_function"
        )
        if entry in talon_list:
            ui.label(f"{i}. {entry}: {talon_list[entry]}")

    ui_wrapper.spacing()
    if ui_wrapper.command_button("funk close"):
        actions.user.code_toggle_functions()


def commands_updated(_):
    if gui_functions.showing:
        update_function_list()


registry.register("update_commands", commands_updated)
