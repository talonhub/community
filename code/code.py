from talon import Context, Module, actions, app, imgui, registry, settings

ctx = Context()
mod = Module()
mod.list("code_functions", desc="List of functions for active language")
mod.list("code_types", desc="List of types for active language")
mod.list("code_libraries", desc="List of libraries for active language")

setting_private_function_formatter = mod.setting("code_private_function_formatter", str)
setting_protected_function_formatter = mod.setting(
    "code_protected_function_formatter", str
)
setting_public_function_formatter = mod.setting("code_public_function_formatter", str)
setting_private_variable_formatter = mod.setting("code_private_variable_formatter", str)
setting_protected_variable_formatter = mod.setting(
    "code_protected_variable_formatter", str
)
setting_public_variable_formatter = mod.setting("code_public_variable_formatter", str)

mod.tag("code_comment", desc="Tag for enabling generic comment commands")
mod.tag("code_block_comment", desc="Tag for enabling generic block comment commands")
mod.tag("code_operators", desc="Tag for enabling generic operator commands")
mod.tag(
    "code_generic",
    desc="Tag for enabling other basic programming commands (loops, functions, etc)",
)

key = actions.key
function_list = []
library_list = []
extension_lang_map = {
    ".asm": "assembly",
    ".bat": "batch",
    ".c": "c",
    ".cmake": "cmake",
    ".cpp": "cplusplus",
    ".cs": "csharp",
    ".gdb": "gdb",
    ".go": "go",
    ".h": "c",
    ".hpp": "cplusplus",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript",
    ".json": "json",
    ".lua": "lua",
    ".md": "markdown",
    ".pl": "perl",
    ".ps1": "powershell",
    ".py": "python",
    ".r": "r",
    ".rb": "ruby",
    ".s": "assembly",
    ".sh": "bash",
    ".snippets": "snippets",
    ".talon": "talon",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".vba": "vba",
    ".vim": "vimscript",
    ".vimrc": "vimscript",
}

# flag indicates whether or not the title tracking is enabled
forced_language = False


@mod.capture(rule="{user.code_functions}")
def code_functions(m) -> str:
    """Returns a function name"""
    return m.code_functions


@mod.capture(rule="{user.code_types}")
def code_types(m) -> str:
    """Returns a type"""
    return m.code_types


@mod.capture(rule="{user.code_libraries}")
def code_libraries(m) -> str:
    """Returns a type"""
    return m.code_libraries


@ctx.action_class("code")
class code_actions:
    def language():
        result = ""
        if not forced_language:
            file_extension = actions.win.file_ext()

            if file_extension and file_extension in extension_lang_map:
                result = extension_lang_map[file_extension]

        # print("code.language: " + result)
        return result


# create a mode for each defined language
for __, lang in extension_lang_map.items():
    mod.mode(lang)


@mod.action_class
class Actions:
    def code_set_language_mode(language: str):
        """Sets the active language mode, and disables extension matching"""
        global forced_language
        actions.user.code_clear_language_mode()
        actions.mode.enable("user.{}".format(language))
        # app.notify("Enabled {} mode".format(language))
        forced_language = True

    def code_clear_language_mode():
        """Clears the active language mode, and re-enables code.language: extension matching"""
        global forced_language
        forced_language = False

        for __, lang in extension_lang_map.items():
            actions.mode.disable("user.{}".format(lang))
        # app.notify("Cleared language modes")

    def code_operator_indirection():
        """code_operator_indirection"""

    def code_operator_address_of():
        """code_operator_address_of (e.g., C++ & op)"""

    def code_operator_structure_dereference():
        """code_operator_structure_dereference (e.g., C++ -> op)"""

    def code_operator_lambda():
        """code_operator_lambda"""

    def code_operator_subscript():
        """code_operator_subscript (e.g., C++ [])"""

    def code_operator_assignment():
        """code_operator_assignment"""

    def code_operator_subtraction():
        """code_operator_subtraction"""

    def code_operator_subtraction_assignment():
        """code_operator_subtraction_equals"""

    def code_operator_addition():
        """code_operator_addition"""

    def code_operator_addition_assignment():
        """code_operator_addition_assignment"""

    def code_operator_multiplication():
        """code_operator_multiplication"""

    def code_operator_multiplication_assignment():
        """code_operator_multiplication_assignment"""

    def code_operator_exponent():
        """code_operator_exponent"""

    def code_operator_division():
        """code_operator_division"""

    def code_operator_division_assignment():
        """code_operator_division_assignment"""

    def code_operator_modulo():
        """code_operator_modulo"""

    def code_operator_modulo_assignment():
        """code_operator_modulo_assignment"""

    def code_operator_equal():
        """code_operator_equal"""

    def code_operator_not_equal():
        """code_operator_not_equal"""

    def code_operator_greater_than():
        """code_operator_greater_than"""

    def code_operator_greater_than_or_equal_to():
        """code_operator_greater_than_or_equal_to"""

    def code_operator_less_than():
        """code_operator_less_than"""

    def code_operator_less_than_or_equal_to():
        """code_operator_less_than_or_equal_to"""

    def code_operator_in():
        """code_operator_less_than_or_equal_to"""

    def code_operator_and():
        """codee_operator_and"""

    def code_operator_or():
        """code_operator_or"""

    def code_operator_bitwise_and():
        """code_operator_bitwise_and"""

    def code_operator_bitwise_and_assignment():
        """code_operator_and"""

    def code_operator_bitwise_or():
        """code_operator_bitwise_or"""

    def code_operator_bitwise_or_assignment():
        """code_operator_or_assignment"""

    def code_operator_bitwise_exclusive_or():
        """code_operator_bitwise_exclusive_or"""

    def code_operator_bitwise_exclusive_or_assignment():
        """code_operator_bitwise_exclusive_or_assignment"""

    def code_operator_bitwise_left_shift():
        """code_operator_bitwise_left_shift"""

    def code_operator_bitwise_left_shift_assignment():
        """code_operator_bitwise_left_shift_assigment"""

    def code_operator_bitwise_right_shift():
        """code_operator_bitwise_right_shift"""

    def code_operator_bitwise_right_shift_assignment():
        """code_operator_bitwise_right_shift_assignment"""

    def code_block():
        """Inserts equivalent of {\n} for the active language, and places the cursor appropriately"""

    def code_self():
        """Inserts the equivalent of "this" in C++ or self in python"""

    def code_null():
        """inserts null equivalent"""

    def code_is_null():
        """inserts check for == null"""

    def code_is_not_null():
        """inserts check for == null"""

    def code_state_in():
        """Inserts python "in" equivalent"""

    def code_state_if():
        """Inserts if statement"""

    def code_state_else_if():
        """Inserts else if statement"""

    def code_state_else():
        """Inserts else statement"""

    def code_state_do():
        """Inserts do statement"""

    def code_state_switch():
        """Inserts switch statement"""

    def code_state_case():
        """Inserts case statement"""

    def code_state_for():
        """Inserts for statement"""

    def code_state_for_each():
        """Inserts for each equivalent statement"""

    def code_state_go_to():
        """inserts go-to statement"""

    def code_state_while():
        """Inserts while statement"""

    def code_state_return():
        """Inserts return statement"""

    def code_break():
        """Inserts break statement"""

    def code_next():
        """Inserts next statement"""

    def code_true():
        """Insert True value"""

    def code_false():
        """Insert False value"""

    def code_try_catch():
        """Inserts try/catch. If selection is true, does so around the selecion"""

    def code_default_function(text: str):
        """Inserts function declaration"""
        actions.user.code_private_function(text)

    def code_private_function(text: str):
        """Inserts private function declaration"""

    def code_private_static_function(text: str):
        """Inserts private static function"""

    def code_protected_function(text: str):
        """Inserts protected function declaration"""

    def code_protected_static_function(text: str):
        """Inserts public function"""

    def code_public_function(text: str):
        """Inserts public function"""

    def code_public_static_function(text: str):
        """Inserts public function"""

    def code_private_function_formatter(name: str):
        """Inserts private function name with formatter"""
        actions.insert(
            actions.user.formatted_text(
                name, settings.get("user.code_private_function_formatter")
            )
        )

    def code_protected_function_formatter(name: str):
        """inserts properly formatted private function name"""
        actions.insert(
            actions.user.formatted_text(
                name, settings.get("user.code_protected_function_formatter")
            )
        )

    def code_public_function_formatter(name: str):
        """inserts properly formatted private function name"""
        actions.insert(
            actions.user.formatted_text(
                name, settings.get("user.code_public_function_formatter")
            )
        )

    def code_private_variable_formatter(name: str):
        """inserts properly formatted private function name"""
        actions.insert(
            actions.user.formatted_text(
                name, settings.get("user.code_private_variable_formatter")
            )
        )

    def code_protected_variable_formatter(name: str):
        """inserts properly formatted private function name"""
        actions.insert(
            actions.user.formatted_text(
                name, settings.get("user.code_protected_variable_formatter")
            )
        )

    def code_public_variable_formatter(name: str):
        """inserts properly formatted private function name"""
        actions.insert(
            actions.user.formatted_text(
                name, settings.get("user.code_public_variable_formatter")
            )
        )

    def code_comment():
        """Inserts comment at current cursor location"""

    def code_block_comment():
        """Block comment"""

    def code_block_comment_prefix():
        """Block comment start syntax"""

    def code_block_comment_suffix():
        """Block comment end syntax"""

    def code_type_definition():
        """code_type_definition (typedef)"""

    def code_typedef_struct():
        """code_typedef_struct (typedef)"""

    def code_type_class():
        """code_type_class"""

    def code_type_struct():
        """code_type_struct"""

    def code_include():
        """code_include"""

    def code_include_system():
        """code_include_system"""

    def code_include_local():
        """code_include_local"""

    def code_import():
        """import/using equivalent"""

    def code_from_import():
        """from import python equivalent"""

    def code_toggle_functions():
        """GUI: List functions for active language"""
        global function_list
        if gui_libraries.showing:
            gui_libraries.hide()
        if gui_functions.showing:
            function_list = []
            gui_functions.hide()
        else:
            update_function_list_and_freeze()

    def code_select_function(number: int, selection: str):
        """Inserts the selected function when the imgui is open"""
        if gui_functions.showing and number < len(function_list):
            actions.user.code_insert_function(
                registry.lists["user.code_functions"][0][function_list[number]],
                selection,
            )

    def code_insert_function(text: str, selection: str):
        """Inserts a function and positions the cursor appropriately"""

    def code_toggle_libraries():
        """GUI: List libraries for active language"""
        global library_list
        if gui_functions.showing:
            gui_functions.hide()
        if gui_libraries.showing:
            library_list = []
            gui_libraries.hide()
        else:
            update_library_list_and_freeze()

    def code_select_library(number: int, selection: str):
        """Inserts the selected library when the imgui is open"""
        if gui_libraries.showing and number < len(library_list):
            actions.user.code_insert_library(
                registry.lists["user.code_libraries"][0][library_list[number]],
                selection,
            )

    def code_insert_library(text: str, selection: str):
        """Inserts a library and positions the cursor appropriately"""

    def code_document_string():
        """Inserts a document string and positions the cursor appropriately"""


def update_library_list_and_freeze():
    global library_list
    if "user.code_libraries" in registry.lists:
        library_list = sorted(registry.lists["user.code_libraries"][0].keys())
    else:
        library_list = []

    gui_libraries.show()


def update_function_list_and_freeze():
    global function_list
    if "user.code_functions" in registry.lists:
        function_list = sorted(registry.lists["user.code_functions"][0].keys())
    else:
        function_list = []

    gui_functions.show()


@imgui.open()
def gui_functions(gui: imgui.GUI):
    gui.text("Functions")
    gui.line()

    # print(str(registry.lists["user.code_functions"]))
    for i, entry in enumerate(function_list, 1):
        if entry in registry.lists["user.code_functions"][0]:
            gui.text(
                "{}. {}: {}".format(
                    i, entry, registry.lists["user.code_functions"][0][entry]
                )
            )


@imgui.open()
def gui_libraries(gui: imgui.GUI):
    gui.text("Libraries")
    gui.line()

    for i, entry in enumerate(library_list, 1):
        gui.text(
            "{}. {}: {}".format(
                i, entry, registry.lists["user.code_libraries"][0][entry]
            )
        )


def commands_updated(_):
    if gui_functions.showing:
        update_function_list_and_freeze()
    if gui_libraries.showing:
        update_library_list_and_freeze()


registry.register("update_commands", commands_updated)
