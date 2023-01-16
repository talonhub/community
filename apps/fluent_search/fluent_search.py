from talon import Module, actions


mod = Module()
mod.apps.fluent_search = """
os: windows
and app.name: FluentSearch
os: windows
and app.exe: FluentSearch.exe
"""
mod.tag("fluent_search_screen_search")


@mod.action_class
class Actions:
    def fluent_search_screen_search(letters: str, mouse_action: str):
        """Search in fluent_search"""
        action = ""
        if "right" == mouse_action:
            action = "4"
        elif "double" == mouse_action:
            action = "2"
        elif "triple" == mouse_action:
            action = "3"
        elif "hover" == mouse_action:
            action = "5"
        keys = " ".join(action + letters)

        actions.key(keys)
