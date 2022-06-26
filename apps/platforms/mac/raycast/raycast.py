from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.list("raycast_command", desc="Raycast commands")
ctx.lists["user.raycast_command"] = {
    "schedule": "My Schedule",
    "jira open": "Jira Open Issues",
    "jira create": "Jira Create Issue",
}

mod.list("raycast_input_command", desc="Raycast commands which accept input")
ctx.lists["user.raycast_input_command"] = {
    "google": "Search Google",
    "code": "Recent Projects",
    "pulls": "GitHub Enterprise Open Pull Requests",
    "repos": "GitHub Search Repositories",
    "jira search": "Jira Search Issues",
    "brew search": "Brew Search",
}


@mod.action_class
class Actions:
    def raycast(command: str = "", input: str or None = None):
        """Launch Raycast command with optional input"""
        actions.key("cmd-space")
        actions.sleep("150ms")
        if command:
            actions.insert(command)
        if input is not None:
            actions.key("tab")
        if input:
            actions.sleep("150ms")
            actions.insert(input)


@ctx.action("user.switcher_menu")
def open_raycast_switcher():
    actions.key("alt-space")
