from talon import Module, actions

mod = Module()

mod.list("html_attribute", "List of common HTML attributes")


@mod.action_class
class Actions:
    def insert_html_attribute(name: str):
        """Insert an HTML attribute with a leading space and cursor inside the quotes."""
        actions.user.insert_between(f' {name}="', '"')
