from talon import Context, actions, ui, Module, app

mod = Module()
mod.tag("poetry", desc="Tag for enabling generic terminal commands")
mod.apps.poetry = """
tag: user.poetry
"""
mod.list("poetry_commands", desc="poetry CLI Commands")

commands = {
    "add": "add ",
    "search": "search ",
    "show": "show ",
    "help": "--help\n",
    "shell": "shell\n",
    "install": "install\n",
}
ctx = Context()
ctx.matches = r"""
app: poetry
"""


ctx.lists["self.poetry_commands"] = commands


# @mod.action_class
# class Actions:
#     def function_name():
#         """This description is mandatory"""
