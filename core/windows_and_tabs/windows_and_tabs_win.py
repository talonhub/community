# defines the default app actions for windows

from talon import Context, actions, ui

ctx = Context()
ctx.matches = r"""
os: windows
"""

SYSTEM_MENU_SHORTCUT_MULTISTEP_DELAY = "50ms"


@ctx.action_class("app")
class AppActions:
    # app.preferences()

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
            window.close()
        else:
            actions.key("alt-f4")

    def window_hide():
        if window := ui.active_window():
            window.minimized = True
        else:
            actions.key("alt-space")
            actions.sleep(SYSTEM_MENU_SHORTCUT_MULTISTEP_DELAY)
            actions.key("n")  # Depends on English OS language.

    def window_hide_others():
        actions.key("win-d alt-tab")

    def window_open():
        actions.key("ctrl-n")


@ctx.action_class("user")
class UserActions:
    def switcher_focus_last():
        actions.key("alt-tab")

    def window_maximize():
        if window := ui.active_window():
            window.maximized = True
        else:
            actions.key("alt-space")
            actions.sleep(SYSTEM_MENU_SHORTCUT_MULTISTEP_DELAY)
            actions.key("x")  # Depends on English OS language.

    def window_restore():
        if window := ui.active_window():
            window.maximized = False
        else:
            actions.key("alt-space")
            actions.sleep(SYSTEM_MENU_SHORTCUT_MULTISTEP_DELAY)
            actions.key("r")  # Depends on English OS language.
