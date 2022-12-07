import talon.mac.ui  # ActionFailed
from talon import Context, actions, ui

ctx = Context()
ctx.matches = r"""
os: mac
"""


@ctx.action_class("app")
class AppActions:
    def preferences():
        actions.key("cmd-,")

    def tab_close():
        actions.key("cmd-w")
        # action(app.tab_detach):
        #  Move the current tab to a new window

    def tab_next():
        actions.key("cmd-shift-]")

    def tab_open():
        actions.key("cmd-t")

    def tab_previous():
        actions.key("cmd-shift-[")

    def tab_reopen():
        actions.key("cmd-shift-t")

    def window_close():
        # Try to use accessibility, but fall back on cmd-w.
        try:
            w = ui.active_window()
            button = w.element["AXCloseButton"]
            assert button.actions["AXPress"] == "press"
        except Exception as e:
            actions.key("cmd-w")
        else:
            # This can fail with talon.mac.ui.ActionFailed if the window opens a
            # confirmation dialog. But pressing cmd-w or clicking the close
            # button would do the same, so we don't regard this as failure.
            try:
                button.perform("AXPress")
            except talon.mac.ui.ActionFailed:
                pass

    def window_hide():
        actions.key("cmd-m")

    def window_hide_others():
        actions.key("cmd-alt-h")

    def window_next():
        actions.key("cmd-`")

    def window_open():
        actions.key("cmd-n")

    def window_previous():
        actions.key("cmd-shift-`")
