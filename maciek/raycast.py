from talon import Context, actions, ui, Module, app

mod = Module()


def wait_for_raycast():
    actions.sleep("200ms")


@mod.action_class
class user_actions:
    def raycast_summon():
        """."""
        pass

    def raycast_talon_search(query: str):
        """."""
        actions.key("cmd-shift-f1")
        wait_for_raycast()
        actions.insert(query)

    def raycast_raindrop_search(query: str):
        """."""
        actions.key("cmd-shift-f4")
        wait_for_raycast()
        actions.insert(query)

    def raycast_clipboard():
        """."""
        actions.key("cmd-shift-f7")

    def raycast_coder_project(project_name: str):
        """."""
        actions.key("cmd-shift-f2")
        wait_for_raycast()
        actions.insert(project_name)
        if project_name:
            actions.key("enter")
