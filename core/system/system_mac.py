from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
"""


@ctx.action_class("user")
class UserActions:
    def system_switch_screen_power(on: bool):
        # TODO
        pass

    def system_show_settings():
        # TODO
        pass

    def system_show_task_manager():
        # TODO
        pass

    def system_lock():
        # TODO
        pass

    def system_show_exit_menu():
        # TODO: Idea from Windows user: Maybe show Apple menu and simulate arrow key up to get to the lower menu entries.
        pass
