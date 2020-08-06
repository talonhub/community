# defines placeholder actions and captures for ide-specific snippet functionality
from talon import Module, actions, app, Context

mod = Module()
ctx = Context()
mod.tag("snippets", desc="Tag for enabling code snippet-related commands")
mod.list("snippets", desc="List of code snippets")


@mod.capture
def snippets(m) -> list:
    """Returns a snippet name"""


@mod.action_class
class Actions:
    def snippet_search(text: str):
        """Triggers the program's snippet search"""

    def snippet_insert(text: str):
        """Inserts a snippet"""

    def snippet_create():
        """Triggers snippet creation"""


@ctx.capture(rule="{user.snippets}")
def snippets(m):
    return m.snippets

