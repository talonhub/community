from talon import Context, Module, actions, imgui, registry

ctx = Context()
mod = Module()

mod.list("code_libraries", desc="List of libraries for active language")
mod.tag(
    "code_libraries_gui_showing", desc="Active when the library picker GUI is showing"
)

# global
library_list = []


@mod.capture(rule="{user.code_libraries}")
def code_libraries(m) -> str:
    """Returns a type"""
    return m.code_libraries


mod.tag("code_libraries_gui", desc="Tag for enabling GUI support for common libraries")


@mod.action_class
class Actions:
    def code_toggle_libraries():
        """GUI: List libraries for active language"""
        global library_list
        if gui_libraries.showing:
            library_list = []
            gui_libraries.hide()
            ctx.tags.discard("user.code_libraries_gui_showing")
        else:
            update_library_list_and_freeze()

    def code_select_library(number: int, selection: str):
        """Inserts the selected library when the imgui is open"""
        if gui_libraries.showing and number < len(library_list):
            actions.user.code_insert_library(
                registry.lists["user.code_libraries"][0][library_list[number]],
                selection,
            )

    # TODO: clarify the relation between `code_insert_library`
    #       and `code_import`

    def code_insert_library(text: str, selection: str):
        """Inserts a library and positions the cursor appropriately"""


@imgui.open()
def gui_libraries(gui: imgui.GUI):
    gui.text("Libraries")
    gui.line()

    for i, entry in enumerate(library_list, 1):
        gui.text(f"{i}. {entry}: {registry.lists['user.code_libraries'][0][entry]}")

    gui.spacer()
    if gui.button("Toggle libraries close"):
        actions.user.code_toggle_libraries_hide()


def update_library_list_and_freeze():
    global library_list
    if "user.code_libraries" in registry.lists:
        library_list = sorted(registry.lists["user.code_libraries"][0].keys())
    else:
        library_list = []

    gui_libraries.show()
    ctx.tags.add("user.code_libraries_gui_showing")


def commands_updated(_):
    if gui_libraries.showing:
        update_library_list_and_freeze()


registry.register("update_commands", commands_updated)
