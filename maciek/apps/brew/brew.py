from talon import Context, Module

mod = Module()
mod.tag("brew", desc=".")
mod.apps.brew = """
tag: user.brew
"""
mod.list("brew_commands", desc="Brew CLI Commands")

commands = {
    "help": "--help",
    "info": "info",
    "install": "install",
    "search": "search",
}
ctx = Context()
ctx.matches = r"""
app: brew
"""


ctx.lists["self.brew_commands"] = commands


# @mod.action_class
# class Actions:
#     def function_name():
#         """This description is mandatory"""
