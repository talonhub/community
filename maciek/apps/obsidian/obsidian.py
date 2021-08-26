from talon import Module, actions

mod = Module()
apps = mod.apps
apps.obsidian = "app.name: Obsidian"


@mod.action_class
class Actions:
    def obsidian_run_command(cmd: str):
        """This comment is mandatory"""

        actions.key("cmd-p")
        actions.sleep("20ms")
        actions.insert(cmd)
        actions.sleep("40ms")
        actions.key("enter")
