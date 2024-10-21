from talon import Context, Module, actions, ui

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


def rc(command: str = "", input: str | None = None, wait: bool = True, key: str = "cmd-space"):
    """Launch Raycast command with optional input"""
    def on_focus(win):
        if win.app.name != "Raycast":
            return

        ui.unregister("win_open", on_focus)
        
        if command:
            actions.insert(command)
        if input is not None:
            actions.key("tab")
        if input:
            actions.sleep("150ms")
            actions.insert(input)
        if not wait:
            actions.key("enter")
    
    ui.register("win_open", on_focus)
    actions.key(key)
        
@mod.action_class
class Actions:
    def raycast(command: str = "", input: str | None = None):
        """Execute command immediately with raycast"""
        rc(command, input, False) 
        
    def raycast_wait(command: str = "", input: str | None = None):
        """Input command into raycast and wait"""
        rc(command, input, True)

    def raycast_switcher(name: str = "", wait: bool = False):
        """Switch to window using Raycast"""
        rc(command=name, wait=wait, key="alt-space")
