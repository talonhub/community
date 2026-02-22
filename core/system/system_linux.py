from talon import Context, actions

i3wm_ctx = Context()
i3wm_ctx.matches = r"""
os: linux
tag: user.i3wm
"""


@i3wm_ctx.action_class("user")
class I3wmUserActions:
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
        # Adapt key configuration as needed.
        actions.key("super-shift-x")

    def system_show_exit_menu():
        # TODO
        pass
