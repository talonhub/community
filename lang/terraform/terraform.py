from talon import Context, Module, actions

from ..tags.operators import Operators

ctx = Context()
mod = Module()
ctx.matches = r"""
code.language: terraform
"""

types = {
    "string": "string",
    "number": "number",
    "bool": "bool",
    "list": "list",
    "map": "map",
    "null": "null",
}

ctx.lists["user.code_type"] = types

common_properties = {
    "name": "name",
    "type": "type",
    "description": "description",
    "default": "default",
    "for each": "for_each",
    "count": "count",
    "prevent destroy": "prevent_destroy",
    "nullable": "nullable",
    "sensitive": "sensitive",
    "depends on": "depends_on",
    "provider": "provider",
    "source": "source",
}

mod.list("terraform_common_property", desc="Terraform Modifier")
ctx.lists["self.terraform_common_property"] = common_properties

module_blocks = {
    "variable": "variable",
    "output": "output",
    "provider": "provider",
    "module": "module",
}

mod.list("terraform_module_block", desc="Simple Terraform Block")
ctx.lists["self.terraform_module_block"] = module_blocks

operators = Operators(
    # code_operators_assignment
    ASSIGNMENT=" = ",
    # code_operators_lambda
    LAMBDA=" => ",
    # code_operators_math
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" && ",
    MATH_OR=" || ",
)


@mod.action_class
class Actions:
    def code_terraform_module_block(text: str):
        """Inserts a new module-related block of a given type (e.g. variable, output, provider...)"""

    def code_terraform_resource(text: str):
        """Inserts a new resource block with given name"""

    def code_terraform_data_source(text: str):
        """Inserts a new data block with given name"""


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_terraform_module_block(text: str):
        actions.user.insert_between(text + ' "', '"')

    def code_terraform_resource(text: str):
        result = f"resource \"{actions.user.formatted_text(text, 'SNAKE_CASE')}\" \"\""

        actions.insert(result)
        actions.key("left")

    def code_terraform_data_source(text: str):
        result = f"data \"{actions.user.formatted_text(text, 'SNAKE_CASE')}\" \"\""

        actions.insert(result)
        actions.key("left")

    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

    def code_insert_null():
        actions.insert("null")

    def code_insert_is_null():
        actions.insert(" == null")

    def code_insert_is_not_null():
        actions.insert(" != null")

    def code_comment_line_prefix():
        actions.user.insert_snippet_by_name("commentLine")

    def code_state_for():
        actions.user.insert_snippet_by_name("forLoopStatement")
