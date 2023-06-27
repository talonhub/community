from talon import Context, actions, app

ctx = Context()

ctx.matches = r"""
os: mac
app: vivaldi
"""


@ctx.action_class("user")
class UserActions:
    def vivaldi_history_panel():
        actions.key("cmd-alt-y")

    def vivaldi_downloads_panel():
        actions.key("cmd-alt-l")

    def vivaldi_notes_panel():
        # This shortcut didn't work for me. You might need to change it to a
        # different one.
        actions.key("cmd-alt-n")

    def vivaldi_toggle_quick_commands():
        actions.key("cmd-e")

    def tab_jump(number: int):
        actions.key(f"cmd-{number}")


@ctx.action_class("app")
class AppActions:
    def tab_next():
        actions.key("cmd-shift-]")

    def tab_previous():
        actions.key("cmd-shift-[")


@ctx.action_class("browser")
class BrowserActions:
    def show_extensions():
        actions.key("ctrl-cmd-e")

    def bookmarks():
        actions.key("cmd-ctrl-b")

    def focus_address():
        actions.key("cmd-l")
