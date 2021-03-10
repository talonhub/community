# vs title tracking requires an extension
# https://marketplace.visualstudio.com/items?itemName=mayerwin.RenameVisualStudioWindowTitle
# I currently configure the extension as below
# Document (no solution) open: [documentName] - [ideName]
# No document or solution open: [idleName]
# Solution in break mode: [documentName] - [parentPath]\[solutionName] (Debugging) - [ideName]
# Solution in design mode: [documentName] - [parentPath]\[solutionName] - [ideName]
# Solution in running mode: [documentName] - [parentPath]\[solutionName] (Running) - [ideName]

from talon import Context, actions, ui, Module, app, clip
from typing import List, Union

# is_mac = app.platform == "mac"

ctx = Context()
mod = Module()

apps = mod.apps
apps.visual_studio = """
os: windows
and app.name: Microsoft Visual Studio 2019
os: windows
and app.name: devenv.exe
"""


ctx.matches = r"""
app: visual_studio
"""


@ctx.action_class("win")
class win_actions:
    def filename():
        title = actions.win.title()
        # this doesn't seem to be necessary on VSCode for Mac
        # if title == "":
        #    title = ui.active_window().doc

        result = title.split("-")[0].rstrip()

        if "." in result:
            # print(result)
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
        actions.key("ctrl-d")

    def jump_line(n: int):
        actions.key("ctrl-g")
        actions.sleep("100ms")
        actions.insert(str(n))
        actions.key("enter")


@ctx.action_class("user")
class user_actions:
    # snippet.py support beginHelp close
    def snippet_search(text: str):
        """TEST"""
        actions.key("ctrl-k ctrl-x")

    # def snippet_insert(text: str):
    #     """Inserts a snippet"""

    # def snippet_create():
    #     """Triggers snippet creation"""

    # snippet.py support end

    # def select_word(verb: str):
    #     actions.key("ctrl-w")
    #     actions.user.perform_selection_action(verb)

    # def select_next_occurrence(verbs: str, text: str):
    #     actions.edit.find(text)
    #     actions.sleep("100ms")

    #     actions.key("esc")
    #     if verbs is not None:
    #         actions.user.perform_selection_action(verbs)

    # def select_previous_occurrence(verbs: str, text: str):
    #     actions.edit.find(text)
    #     actions.key("shift-enter")
    #     actions.sleep("100ms")
    #     actions.key("esc")
    #     if verbs is not None:
    #         actions.user.perform_selection_action(verbs)

    # def go_to_line(verb: str, line: int):
    #     actions.key("ctrl-g")
    #     actions.insert(str(line))
    #     actions.key("enter")

    #     if verb is not None:
    #         actions.user.perform_movement_action(verb)

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
    # if index < 9:
    #     if is_mac:
    #         actions.key("cmd-{}".format(index))
    #     else:
    #         actions.key("ctrl-{}".format(index))

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
        actions.key("ctrl-shift-f")

        if text:
            actions.insert(text)

    def find_toggle_match_by_case():
        """Toggles find match by case sensitivity"""
        actions.key("alt-c")

    def find_toggle_match_by_word():
        """Toggles find match by whole words"""
        actions.key("alt-w")

    def find_toggle_match_by_regex():
        """Toggles find match by regex"""
        actions.key("alt-r")

    def replace(text: str):
        """Search and replaces in the active editor"""
        actions.key("ctrl-h")

        if text:
            actions.insert(text)

    def replace_everywhere(text: str):
        """Search and replaces in the entire project"""
        actions.key("ctrl-shift-h")

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
        actions.key("shift-enter")
        actions.sleep("100ms")
        actions.key("esc")

    def select_next_occurrence(text: str):
        actions.edit.find(text)
        actions.sleep("100ms")
        actions.key("esc")

    # find_and_replace.py support end

