from talon import Module, ui, actions

mod = Module()

mod.tag("plugins", "Enable commands and contexts for apps that use optional plugins")

@mod.scope
def scope():
    return {"plugin_installed": actions.user.plugins_list()}

@mod.action_class
class Actions:
    def plugins_scope_update():
        """Update the scope for the plugins module

        This is not meant to be overridden, but rather is a way for applications
        to be able to update the scope when needed."""

        scope.update()

    def plugins_list() -> set:
        """Returns a set of plugins associated with the active app"""
        return set()

    def plugins_list_refresh() -> str:
        """Refresh the list of plugins associated with the active app"""

    def plugins_list_print() -> str:
        """Print the list of plugins currently associated with the active app"""

ui.register("win_focus", scope.update)
ui.register("win_title", scope.update)
