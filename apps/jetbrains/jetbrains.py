import os
import os.path
import requests
import time
from pathlib import Path
from talon import ctrl, ui, Module, Context, actions, clip
import tempfile

# Courtesy of https://github.com/anonfunc/talon-user/blob/master/apps/jetbrains.py

extendCommands = []

# Each IDE gets its own port, as otherwise you wouldn't be able
# to run two at the same time and switch between them.
# Note that MPS and IntelliJ ultimate will conflict...
port_mapping = {
    "com.google.android.studio": 8652,
    "com.jetbrains.AppCode": 8655,
    "com.jetbrains.CLion": 8657,
    "com.jetbrains.datagrip": 8664,
    "com.jetbrains.goland-EAP": 8659,
    "com.jetbrains.goland": 8659,
    "com.jetbrains.intellij-EAP": 8653,
    "com.jetbrains.intellij.ce": 8654,
    "com.jetbrains.intellij": 8653,
    "com.jetbrains.PhpStorm": 8662,
    "com.jetbrains.pycharm": 8658,
    "com.jetbrains.rider": 8660,
    "com.jetbrains.rubymine": 8661,
    "com.jetbrains.WebStorm": 8663,
    "google-android-studio": 8652,
    "idea64.exe": 8653,
    "IntelliJ IDEA": 8653,
    "jetbrains-appcode": 8655,
    "jetbrains-clion": 8657,
    "jetbrains-datagrip": 8664,
    "jetbrains-goland-eap": 8659,
    "jetbrains-goland": 8659,
    "jetbrains-idea-ce": 8654,
    "jetbrains-idea-eap": 8653,
    "jetbrains-idea": 8653,
    "jetbrains-phpstorm": 8662,
    "jetbrains-pycharm-ce": 8658,
    "jetbrains-pycharm": 8658,
    "jetbrains-rider": 8660,
    "jetbrains-rubymine": 8661,
    "jetbrains-studio": 8652,
    "jetbrains-webstorm": 8663,
    "PyCharm": 8658,
    "pycharm64.exe": 8658,
    "webstorm64.exe": 8663,
}

select_verbs_map = {
    "clear": ["action EditorBackSpace"],
    "collapse": ["action CollapseRegion"],
    "comment": ["action CommentByLineComment"],
    "copy": ["action EditorCopy"],
    "cut": ["action EditorCut"],
    "drag down": ["action MoveLineDown"],
    "drag up": ["action MoveLineUp"],
    "expand": ["action ExpandRegion"],
    "indent": ["action EditorIndentLineOrSelection"],
    "refactor": ["action Refactorings.QuickListPopupAction"],
    "rename": ["action RenameElement"],
    "replace": ["action EditorPaste"],
    "select": [],
    "unindent": ["action EditorUnindentSelection"],
}

movement_verbs_map = {
    "fix": ["action ShowIntentionActions"],
    "go": [],
    "paste": ["action EditorPaste"],
}


def set_extend(*commands):
    def set_inner(_):
        global extendCommands
        extendCommands = commands

    return set_inner


def _get_nonce(port, file_prefix):
    file_name = file_prefix + str(port)
    try:
        with open(os.path.join(tempfile.gettempdir(), file_name), "r") as fh:
            return fh.read()
    except FileNotFoundError as e:
        try:
            home = str(Path.home())
            with open(os.path.join(home, file_name), "r") as fh:
                return fh.read()
        except FileNotFoundError as eb:
            print(f"Could not find {file_name} in tmp or home")
            return None
    except IOError as e:
        print(e)
        return None


def send_idea_command(cmd):
    print("Sending {}".format(cmd))
    active_app = ui.active_app()
    bundle = active_app.bundle or active_app.name
    port = port_mapping.get(bundle, None)
    nonce = _get_nonce(port, ".vcidea_") or _get_nonce(port, "vcidea_")
    print(f"sending {bundle} {port} {nonce}")
    if port and nonce:
        response = requests.get(
            "http://localhost:{}/{}/{}".format(port, nonce, cmd), timeout=(0.05, 3.05)
        )
        response.raise_for_status()
        return response.text


def get_idea_location():
    return send_idea_command("location").split()


def idea_commands(commands):
    command_list = commands.split(",")
    print("executing jetbrains", commands)
    global extendCommands
    extendCommands = command_list
    for cmd in command_list:
        if cmd:
            send_idea_command(cmd.strip())
            time.sleep(0.1)


ctx = Context()
mod = Module()

mod.list("select_verbs", desc="Verbs for selecting in the IDE")
mod.list("movement_verbs", desc="Verbs for navigating the IDE")


@mod.action_class
class Actions:
    def idea(commands: str):
        """Send a command to Jetbrains product"""
        idea_commands(commands)

    def idea_select(select_verb: str, commands: str):
        """Do a select command, then the specified commands"""
        command_list = ",".join(commands.split(",") + select_verbs_map[select_verb])
        print(command_list)
        idea_commands(command_list)

    def idea_movement(movement_verb: str, commands: str):
        """Do a select movement, then the specified commands"""
        command_list = ",".join(commands.split(",") + movement_verbs_map[movement_verb])
        print(command_list)
        idea_commands(command_list)

    def idea_grab(times: int):
        """Copies specified number of words to the left"""
        old_clip = clip.get()
        try:
            original_line, original_column = get_idea_location()
            for _ in range(times):
                send_idea_command("action EditorSelectWord")
            send_idea_command("action EditorCopy")
            send_idea_command("goto {} {}".format(original_line, original_column))
            send_idea_command("action EditorPaste")
        finally:
            clip.set(old_clip)
            global extendCommands
            extendCommands = []

    def extend_action(number: str):
        """Repeat previous actions up to number of times"""
        global extendCommands
        count = max(int(number), 1)
        for _ in range(count):
            for cmd in extendCommands:
                send_idea_command(cmd)

    def set_extended_actions(commands: str):
        """Adds specified commands to the list of commands to repeat"""
        set_extend(commands.split(","))


ctx.matches = r"""
app: /jetbrains/
app: IntelliJ IDEA
app: idea64.exe
app: PyCharm
app: PyCharm64.exe
app: pycharm64.exe
app: webstorm64.exe
"""


@ctx.action_class("user")
class user_actions:
    def tab_jump(number: int):
        if number < 10:
            actions.user.idea("action GoToTab{}".format(number))

    def perform_selection_action(verb: str):
        """Performs selection action defined for context"""
        acts = select_verbs_map[verb]
        for act in acts:
            act()

    def perform_movement_action(verb: str):
        """Performs movement action defined for context"""
        acts = movement_verbs_map[verb]
        for act in acts:
            act()

    def select_next_occurrence(verbs: str, text: str):
        actions.user.idea_select(verbs, "find next {}".format(text))

    def select_previous_occurrence(verbs: str, text: str):
        actions.user.idea_select(verbs, "find prev {}".format(text))

    def move_next_occurrence(verbs: str, text: str):
        actions.user.idea_movement(
            verbs, "find next {}, action EditorRight".format(text)
        )

    def move_previous_occurrence(verbs: str, text: str):
        actions.user.idea_select(verbs, "find prev {}, action EditorRight".format(text))

    def go_to_line(verb: str, line: int):
        actions.user.idea_movement(verb, "goto {} 0".format(line))

    def go_to_line_end(verb: str, line: int):
        actions.user.idea_movement(verb, "goto {} 9999".format(line))

    def select_word(verb: str):
        actions.user.idea_select(verb, "action EditorSelectWord")

    def select_whole_line(verb: str, line: int):
        actions.user.idea_select(
            verb, "goto {} 0, action EditorSelectLine".format(line)
        )

    def select_current_line(verb: str):
        actions.user.idea_select(
            verb, "action EditorLineStart, action EditorLineEndWithSelection"
        )

    def select_line(verb: str, line: int):
        actions.user.idea_select(
            verb,
            "goto {} 0, action EditorLineStart, action EditorLineEndWithSelection".format(
                line
            ),
        )

    def select_until_line(verb: str, line: int):
        actions.user.idea_select(verb, "extend {}".format(line))

    def select_range(verb: str, line_start: int, line_end: int):
        actions.user.idea_select(verb, "range {} {}".format(line_start, line_end))

    def select_way_left(verb: str):
        actions.user.idea_select(verb, "action EditorLineStartWithSelection")

    def select_way_right(verb: str):
        actions.user.idea_select(verb, "action EditorLineEndWithSelection")

    def select_way_up(verb: str):
        actions.user.idea_select(verb, "action EditorTextStartWithSelection")

    def select_way_down(verb: str):
        actions.user.idea_select(verb, "action EditorTextEndWithSelection")

    def select_camel_left(verb: str):
        actions.user.idea_select(
            verb, "action EditorPreviousWordInDifferentHumpsModeWithSelection"
        )

    def select_camel_right(verb: str):
        actions.user.idea_select(
            verb, "action EditorNextWordInDifferentHumpsModeWithSelection"
        )

    def select_all(verb: str):
        actions.user.idea_select(verb, "action $SelectAll")

    def select_left(verb: str):
        actions.user.idea_select(verb, "action EditorLeftWithSelection")

    def select_right(verb: str):
        actions.user.idea_select(verb, "action EditorRightWithSelection")

    def select_up(verb: str):
        actions.user.idea_select(verb, "action EditorUpWithSelection")

    def select_down(verb: str):
        actions.user.idea_select(verb, "action EditorDownWithSelection")

    def select_word_left(verb: str):
        actions.user.idea_select(verb, "action EditorPreviousWordWithSelection")

    def select_word_right(verb: str):
        actions.user.idea_select(verb, "action EditorNextWordWithSelection")

    def move_camel_left(verb: str):
        actions.user.idea_movement(
            verb, "action EditorPreviousWordInDifferentHumpsMode"
        )

    def move_camel_right(verb: str):
        actions.user.idea_movement(verb, "action EditorNextWordInDifferentHumpsMode")

    def line_clone(line: int):
        actions.user.idea("clone {}".format(line))


ctx.lists["user.selection_verbs"] = select_verbs_map.keys()
ctx.lists["user.navigation_verbs"] = movement_verbs_map.keys()

