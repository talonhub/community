from typing import Union

from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()

# TODO: abstract visibilities using a list (#663)

mod.tag("code_functions", desc="Tag for enabling commands for functions")

mod.list("code_type", desc="List of types for active language")
mod.list(
    "code_parameter_name", desc="List of common parameter names for active language"
)
mod.list(
    "code_function_modifier",
    desc="List of function modifiers (e.g. private, async, static)",
)

ctx.lists["user.code_function_modifier"] = {
    "pub": "public",
    "pro": "protected",
    "private": "private",
    "static": "static",
}


@mod.capture(rule="{user.code_type}")
def code_type(m) -> str:
    """Returns a macro name"""
    return m.code_type


mod.setting("code_private_function_formatter", str)
mod.setting("code_protected_function_formatter", str)
mod.setting("code_public_function_formatter", str)
mod.setting("code_private_variable_formatter", str)
mod.setting("code_protected_variable_formatter", str)
mod.setting("code_public_variable_formatter", str)


@mod.action_class
class Actions:
    def code_modified_function(modifiers: Union[list[str], int], text: str):
        """
        Inserts function declaration with the given modifiers. modifiers == 0
        implies no modifiers (.talon files don't have empty list literal
        syntax)
        """
        mods = {} if modifiers == 0 else set(modifiers)

        if mods == {}:
            return actions.user.code_default_function(text)
        elif mods == {"static"}:
            return actions.user.code_private_static_function(text)
        elif mods == {"private"}:
            return actions.user.code_private_function(text)
        elif mods == {"private", "static"}:
            return actions.user.code_private_static_function(text)
        elif mods == {"protected"}:
            return actions.user.code_protected_function(text)
        elif mods == {"protected", "static"}:
            return actions.user.code_protected_static_function(text)
        elif mods == {"public"}:
            return actions.user.code_public_function(text)
        elif mods == {"public", "static"}:
            return actions.user.code_public_static_function(text)
        else:
            raise RuntimeError(f"Unhandled modifier set: {mods}")

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

    def code_insert_type_annotation(type: str):
        """Inserts a type annotation"""

    def code_insert_return_type(type: str):
        """Inserts a return type"""

    def code_insert_named_argument(parameter_name: str):
        """Inserts a named argument"""
