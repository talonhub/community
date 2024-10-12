from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.apps.eclipse = """
os: windows
and app.name: eclipse.exe
"""

ctx.matches = r"""
app: eclipse
"""


@ctx.action_class("app")
class AppActions:
    # talon app actions
    def tab_close():
        actions.key("ctrl-w")

    def tab_next():
        actions.key("ctrl-pagedown")

    def tab_previous():
        actions.key("ctrl-pageup")

    # action(app.tab_reopen):
    def window_close():
        actions.key("alt-f4")

    def window_open():
        actions.key("alt-w n")


@ctx.action_class("code")
class CodeActions:
    # talon code actions
    def toggle_comment():
        actions.key("ctrl-7")


@ctx.action_class("edit")
class EditActions:
    def find_next():
        actions.key("enter")

    def find_previous():
        actions.key("shift-enter")

    def line_swap_up():
        actions.key("alt-up")

    def line_swap_down():
        actions.key("alt-down")

    def line_clone():
        actions.key("ctrl-alt-down")

    def jump_line(n: int):
        actions.key("ctrl-l")
        actions.insert(str(n))
        actions.key("enter")

    def delete_line():
        actions.key("ctrl-d")

    def indent_more():
        actions.key("tab")

    def indent_less():
        actions.key("shift-tab")

    def save_all():
        actions.key("ctrl-shift-s")


@ctx.action_class("user")
class UserActions:
    # splits.py support begin
    # requires https://marketplace.eclipse.org/content/handysplit
    def split_clear_all():
        actions.key("alt-shift-s f")

    def split_clear():
        actions.key("alt-shift-s f")

    # action(user.split_flip):
    def split_last():
        actions.key("alt-shift-s t")

    def split_next():
        actions.key("alt-shift-s t")

    def split_window_down():
        actions.key("alt-shift-s m")

    def split_window_horizontally():
        actions.key("alt-ctrl-s s")

    def split_window_right():
        actions.key("alt-shift-s m")

    def split_window_up():
        actions.key("alt-shift-s m")

    def split_window_vertically():
        actions.key("alt-shift-s s")

    def split_window():
        actions.key("alt-ctrl-s s")

    # splits.py support end

    # find_and_replace.py support begin

    def find_everywhere(text: str):
        """Triggers find across project"""
        actions.key("ctrl-h")

        if text:
            actions.insert(text)

    # todo: these commands should only be available
    # when it's focused
    def find_toggle_match_by_case():
        """Toggles find match by case sensitivity"""
        actions.key("alt-c")

    def find_toggle_match_by_word():
        """Toggles find match by whole words"""
        actions.key("alt-w")

    def find_toggle_match_by_regex():
        """Toggles find match by regex"""
        actions.key("alt-e")

    def replace(text: str):
        """Search and replaces in the active editor"""
        actions.key("ctrl-f")

        if text:
            actions.insert(text)

    def replace_everywhere(text: str):
        """Search and replaces in the entire project"""
        actions.key("alt-a f")

        if text:
            actions.insert(text)

    def replace_confirm():
        """Confirm replace at current position"""
        actions.key("alt-r")

    def replace_confirm_all():
        """Confirm replace all"""
        actions.key("alt-a")

    def select_previous_occurrence(text: str):
        actions.edit.find(text)
        actions.sleep("100ms")
        actions.key("alt-b alt-f enter esc")

    def select_next_occurrence(text: str):
        actions.edit.find(text)
        actions.sleep("100ms")
        actions.key("alt-f alt-o esc")

    # find_and_replace.py support end
