from talon import Context, Module, actions, ui
from talon.mac import applescript

mod = Module()
ctx = Context()
ctx.matches = r"""
os: mac
"""


@mod.action_class
class Actions:
    def app_hide():
        """Hide the current app"""
        ui.active_app().element.AXHidden = True

    def app_hide_others():
        """Hide all other apps"""
        actions.key("cmd-alt-h")


@ctx.action_class("app")
class AppActions:
    def preferences():
        actions.key("cmd-,")

    def tab_close():
        actions.key("cmd-w")

    def tab_next():
        actions.key("ctrl-tab")

    def tab_open():
        actions.key("cmd-t")

    def tab_previous():
        actions.key("ctrl-shift-tab")

    def tab_reopen():
        actions.key("cmd-shift-t")

    def window_close():
        if window := ui.active_window():
            window.close()
        else:
            actions.key("cmd-w")

    def window_hide():
        if window := ui.active_window():
            window.minimized = True
        else:
            actions.key("cmd-m")

    def window_hide_others():
        # TODO: Currently hides all apps, like `actions.user.app_hide_others()` already does. Correct this to hide windows instead, if useful, or remove it.
        actions.key("cmd-alt-h")

    def window_open():
        actions.key("cmd-n")

    def window_previous():
        actions.key("cmd-shift-`")

    def window_next():
        actions.key("cmd-`")


@ctx.action_class("user")
class UserActions:
    def switcher_focus_last():
        actions.key("cmd-tab")
