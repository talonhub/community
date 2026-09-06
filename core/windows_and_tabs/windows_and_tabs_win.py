# defines the default app actions for windows

from talon import Context, actions, ui

ctx = Context()
ctx.matches = r"""
os: windows
"""

SYSTEM_MENU_SHORTCUT_MULTISTEP_DELAY = "50ms"


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
            window.close()
        else:
            actions.key("alt-f4")

    def window_hide():
        if window := ui.active_window():
            window.minimized = True
        else:
            actions.key("alt-space")
            actions.sleep(SYSTEM_MENU_SHORTCUT_MULTISTEP_DELAY)
            # TODO: This and the other OS-language-dependent mnemonics in this file should be made to depend on a new Windows-only dictionary `OS_LANG_SYSTEM_MENU_MNEMONICS` that's defined per OS language. The current OS language decides what variant will be effective.
            actions.key("n")  # Depends on English OS language.

            # Note that 2x Win+Down not only minimizes the window, but also restores it before that. It would be contrary to user expectations if a window that was previously maximized is in restored state after unminimizing it again. The shortcut also unexpectedly arranges the window differently, if it's in an arranged state like covering an upper quarter or half of the work area.

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

            # Note that Win+Up arranges the window differently instead of maximizing, if it's in an arranged state like covering a lower quarter or half of the work area. This would be contrary to user expectations.

    def window_restore():
        if window := ui.active_window():
            window.maximized = False
        else:
            actions.key("alt-space")
            actions.sleep(SYSTEM_MENU_SHORTCUT_MULTISTEP_DELAY)
            actions.key("r")  # Depends on English OS language.

            # Note that Win+Down on a restored window minimizes it instead of restoring it. This can happen with apps that previously saved the maximized window placement, and then applied it to the window's restored state, e.g., when restarting the app. Besides *possible* tiny differences in the appearance of the window border, the only hint that the window isn't in maximized state, even though it covers the whole work area, will be the title bar's restore button symbol that's only slightly different to the maximize symbol. It would be contrary to user expectations if the respective voice command minimized a window that the user intended to restore. (The shortcut also arranges the window differently or minimizes it instead of being a no-op, if it's in any arranged state.)
