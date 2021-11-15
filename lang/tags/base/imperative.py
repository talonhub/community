from talon import Context, Module, actions, imgui, registry, settings

ctx = Context()
mod = Module()

mod.list("code_type", desc="List of types for active language")
mod.list("code_parameter_name", desc="List of common parameter names for active language")

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

# TODO: factor out object oriented commands from this tag

mod.tag(
    "code_base_imperative",
    desc="Tag for enabling other basic imperative programming commands (loops, functions, etc)",
)

@mod.action_class
class Actions:
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

    def code_insert_type_annotation(type: str):
        """Inserts a type annotation"""

    def code_insert_return_type(type: str):
        """Inserts a return type"""

    def code_insert_named_argument(parameter_name: str):
        """Inserts a named argument"""

    def code_document_string():
        """Inserts a document string and positions the cursor appropriately"""
