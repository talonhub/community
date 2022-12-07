from talon import Context, Module, actions

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
    def postico_execute():
        """Prompt for confirmation to execute"""
        actions.user.on_confirm("Postico Execute", lambda: actions.key("cmd-enter"))

    def postico_confirm_execute():
        """Confirm and execute"""
        actions.user.confirm("Postico Execute")
