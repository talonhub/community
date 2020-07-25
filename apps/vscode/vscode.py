from talon import Context, actions, ui, Module, app
from typing import List, Union

is_mac = app.platform == "mac"

ctx = Context()
mod = Module()

ctx.matches = r"""
app: Code
app: Code - OSS
app: Code
app: Visual Studio Code
app: Code.exe
"""


@ctx.action_class("win")
class win_actions:
    def filename():
        title = actions.win.title()
        # this doesn't seem to be necessary on VSCode for Mac
        # if title == "":
        #    title = ui.active_window().doc

        if is_mac:
            result = title.split(" — ")[0]
        else:
            result = title.split(" - ")[0]

        if "." in result:
            return result

        return ""

    def file_ext():
        return actions.win.filename().split(".")[-1]


@ctx.action_class("edit")
class edit_actions:
    def find(text: str):
        if is_mac:
            actions.key("cmd-f")
        else:
            actions.key("ctrl-f")

        actions.insert(text)

    def line_swap_up():
        actions.key("alt-up")

    def line_swap_down():
        actions.key("alt-down")

    def line_clone():
        actions.key("shift-alt-down")


@ctx.action_class("user")
class user_actions:
    def snippet_search(text: str):
        actions.user.ide_command_palette()
        actions.insert("Insert Snippet")
        actions.key("enter")
        actions.insert(text)

    def snippet_insert(text: str):
        """Inserts a snippet"""
        actions.user.ide_command_palette()
        actions.insert("Insert Snippet")
        actions.key("enter")
        actions.insert(text)
        actions.key("enter")

    def select_word(verb: str):
        if not is_mac:
            actions.key("ctrl-d")
        else:
            actions.key("cmd-d")
        actions.user.perform_selection_action(verb)

    def select_next_occurrence(verbs: str, text: str):
        actions.edit.find(text)
        actions.sleep("100ms")
        actions.key("esc")
        if verbs is not None:
            actions.user.perform_selection_action(verbs)

    def select_previous_occurrence(verbs: str, text: str):
        actions.edit.find(text)
        actions.key("shift-enter")
        actions.sleep("100ms")
        actions.key("esc")
        if verbs is not None:
            actions.user.perform_selection_action(verbs)

    def go_to_line(verb: str, line: int):
        actions.key("ctrl-g")
        actions.insert(str(line))
        actions.key("enter")

        if verb is not None:
            actions.user.perform_movement_action(verb)

    def ide_copy_path():
        actions.user.ide_command_palette()
        actions.insert("File: Copy Path of Active File")
        actions.key("enter")

    def ide_go_mark():
        actions.user.ide_command_palette()
        actions.insert("View: Show Bookmarks")
        actions.key("enter")

    def ide_toggle_mark():
        actions.user.ide_command_palette()
        actions.insert("Bookmarks: Toggle")
        actions.key("enter")

    def ide_go_next_mark():
        actions.user.ide_command_palette()
        actions.insert("Bookmarks: Jump to Next")
        actions.key("enter")

    def ide_go_last_mark():
        actions.user.ide_command_palette()
        actions.insert("Bookmarks: Jump to Previous")
        actions.key("enter")

    def tab_jump(number: int):
        if number < 10:
            if is_mac:
                actions.key("ctrl-{}".format(number))
            else:
                actions.key("alt-{}".format(number))

    def tab_final():
        if is_mac:
            actions.key("ctrl-0")
        else:
            actions.key("alt-0")

    # splits.py support begin
    def split_number(index: int):
        """Navigates to a the specified split"""
        if index < 9:
            if is_mac:
                actions.key("cmd-{}".format(index))
            else:
                actions.key("ctrl-{}".format(index))

    # splits.py support end

    # find_and_replace.py support begin

    def find(text: str):
        """Triggers find in current editor"""
        if is_mac:
            actions.key("cmd-f")
        else:
            actions.key("ctrl-f")

        if text:
            actions.insert(text)

    def find_next():
        actions.key("enter")

    def find_previous():
        actions.key("shift-enter")

    def find_everywhere(text: str):
        """Triggers find across project"""
        if is_mac:
            actions.key("cmd-shift-f")
        else:
            actions.key("ctrl-shift-f")

        if text:
            actions.insert(text)

    def find_toggle_match_by_case():
        """Toggles find match by case sensitivity"""
        if is_mac:
            actions.key("alt-cmd-c")
        else:
            actions.key("alt-c")

    def find_toggle_match_by_word():
        """Toggles find match by whole words"""
        if is_mac:
            actions.key("cmd-alt-w")
        else:
            actions.key("alt-w")

    def find_toggle_match_by_regex():
        """Toggles find match by regex"""
        if is_mac:
            actions.key("cmd-alt-r")
        else:
            actions.key("alt-r")

    def replace(text: str):
        """Search and replaces in the active editor"""
        if is_mac:
            actions.key("alt-cmd-f")
        else:
            actions.key("ctrl-h")

        if text:
            actions.insert(text)

    def replace_everywhere(text: str):
        """Search and replaces in the entire project"""
        if is_mac:
            actions.key("cmd-shift-h")
        else:
            actions.key("ctrl-shift-h")

        if text:
            actions.insert(text)

    def replace_confirm():
        """Confirm replace at current position"""
        if is_mac:
            actions.key("shift-cmd-1")
        else:
            actions.key("ctrl-shift-1")

    def replace_confirm_all():
        """Confirm replace all"""
        if is_mac:
            actions.key("cmd-enter")
        else:
            actions.key("ctrl-alt-enter")

    # find_and_replace.py support end

