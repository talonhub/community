from talon import Context, actions, ui, Module, app, clip
from typing import List, Union

is_mac = app.platform == "mac"

ctx = Context()
mod = Module()

mod.apps.eclipse = """
os: windows
and app.name: eclipse.exe
"""

ctx.matches = r"""
app: eclipse
"""


@ctx.action_class("win")
class win_actions:
    def filename():
        title = actions.win.title()
        # this doesn't seem to be necessary on VSCode for Mac
        # if title == "":
        #    title = ui.active_window().doc

        if " - " in title:
            result = title.split(" - ")[1]
        else:
            result = title

        if "." in result:
            return result

        return ""


@ctx.action_class("edit")
class edit_actions:
    def find(text: str):
        actions.key("ctrl-f")
        actions.insert(text)

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


@ctx.action_class("user")
class user_actions:
    # snippet.py support beginHelp close
    # def snippet_search(text: str):
    #     actions.user.vscode("Insert Snippet")
    #     actions.insert(text)

    # def snippet_insert(text: str):
    #     """Inserts a snippet"""
    #     actions.user.vscode("Insert Snippet")
    #     actions.insert(text)
    #     actions.key("enter")

    # def snippet_create():
    #     """Triggers snippet creation"""
    #     actions.user.vscode("Preferences: Configure User Snippets")

    # snippet.py support end

    # def tab_jump(number: int):
    #     if number < 10:
    #         if is_mac:
    #             actions.key("ctrl-{}".format(number))
    #         else:
    #             actions.key("alt-{}".format(number))

    # def tab_final():
    #     if is_mac:
    #         actions.key("ctrl-0")
    #     else:
    #         actions.key("alt-0")

    # splits.py support begin
    # def split_number(index: int):
    #     """Navigates to a the specified split"""
    #     if index < 9:
    #         if is_mac:
    #             actions.key("cmd-{}".format(index))
    #         else:
    #             actions.key("ctrl-{}".format(index))

    # splits.py support end

    # find_and_replace.py support begin

    def find(text: str):
        """Triggers find in current editor"""

        actions.key("ctrl-f")
        if text:
            actions.insert(text)

    def find_next():
        actions.key("enter")

    def find_previous():
        actions.key("shift-enter")

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

