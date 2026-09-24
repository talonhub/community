# defines the default app actions for linux

from talon import Context, actions, ui

ctx = Context()
ctx.matches = r"""
os: linux
"""


# TODO: Some keyboard shortcuts were obviously just copied from the Windows implementation. Correct what doesn't work.
@ctx.action_class("app")
class AppActions:
    def tab_close():
        actions.key("ctrl-w")

    def tab_next():
        actions.key("ctrl-tab")

    def tab_open():
        actions.key("ctrl-t")

    def tab_previous():
        actions.key("ctrl-shift-tab")

    def tab_reopen():
        actions.key("ctrl-shift-t")

    def window_close():
        if window := ui.active_window():
            # TODO: Does this work on Linux?
            window.close()
        else:
            actions.key("alt-f4")

    def window_hide():
        if window := ui.active_window():
            # TODO: Does this work on Linux?
            window.minimized = True
        else:
            actions.key("alt-space n")

    def window_hide_others():
        actions.key("win-d alt-tab")

    def window_open():
        actions.key("ctrl-n")


@ctx.action_class("user")
class UserActions:
    def switcher_focus_last():
        actions.key("alt-tab")
