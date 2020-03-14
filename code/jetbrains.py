import os
import os.path
import requests
import time
from talon import ctrl, ui, Module, Context, actions, clip

# Courtesy of https://github.com/anonfunc/talon-user/blob/master/apps/jetbrains.py

extendCommands = []

# Each IDE gets its own port, as otherwise you wouldn't be able
# to run two at the same time and switch between them.
# Note that MPS and IntelliJ ultimate will conflict...
port_mapping = {
    "com.jetbrains.intellij": 8653,
    "com.jetbrains.intellij-EAP": 8653,
    "com.jetbrains.intellij.ce": 8654,
    "com.jetbrains.AppCode": 8655,
    "com.jetbrains.CLion": 8657,
    "com.jetbrains.datagrip": 8664,
    "com.jetbrains.goland": 8659,
    "com.jetbrains.goland-EAP": 8659,
    "com.jetbrains.PhpStorm": 8662,
    "com.jetbrains.pycharm": 8658,
    "com.jetbrains.rider": 8660,
    "com.jetbrains.rubymine": 8661,
    "com.jetbrains.WebStorm": 8663,
    "com.google.android.studio": 8652,

    "jetbrains-idea": 8653,
    "jetbrains-idea-eap": 8653,
    "jetbrains-idea-ce": 8654,
    "jetbrains-appcode": 8655,
    "jetbrains-clion": 8657,
    "jetbrains-datagrip": 8664,
    "jetbrains-goland": 8659,
    "jetbrains-goland-eap": 8659,
    "jetbrains-phpstorm": 8662,
    "jetbrains-pycharm": 8658,
    "jetbrains-pycharm-ce": 8658,
    "jetbrains-rider": 8660,
    "jetbrains-rubymine": 8661,
    "jetbrains-webstorm": 8663,
    "google-android-studio": 8652,
}

select_verbs_map = {
    "select": [],
    "copy": ["action EditorCopy"],
    "cut": ["action EditorCut"],
    "clear": ["action EditorBackSpace"],
    "comment": ["action CommentByLineComment"],
    "replace": ["action EditorPaste"],
    "expand": ["action ExpandRegion"],
    "collapse": ["action CollapseRegion"],
    "refactor": ["action Refactorings.QuickListPopupAction"],
    "rename": ["action RenameElement"],
    "indent": ["action EditorIndentLineOrSelection"],
    "unindent": ["action EditorUnindentSelection"],
}


movement_verbs_map = {
    "go": [],
    "fix": ["action ShowIntentionActions"],
    "paste": ["action EditorPaste"],
}


def set_extend(*commands):
    def set_inner(_):
        global extendCommands
        extendCommands = commands

    return set_inner


def _get_nonce(port):
    try:
        with open(os.path.join("/tmp", "vcidea_" + str(port)), "r") as fh:
            return fh.read()
    except IOError:
        return None


def send_idea_command(cmd):
    print("Sending {}".format(cmd))
    bundle = ui.active_app().name
    port = port_mapping.get(bundle, None)
    nonce = _get_nonce(port)
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
@mod.action_class
class Actions:
    def idea(commands: str):
        """Send a command to Jetbrains product"""
        idea_commands(commands)

    def idea_num(command: str, number: str, zero_okay: bool = False):
        """Sends a command with numbers to Jetbrains product"""
        print(number)
        if int(number) == 0 and not zero_okay:
            print("Not sending, arg was 0")
            return

        formatted = command % number
        send_idea_command(formatted)
        global extendCommands
        extendCommands = []

    def idea_grab(times: str = "1"):
        """Copies specified number of words to the left"""
        old_clip = clip.get()
        try:
            original_line, original_column = get_idea_location()
            for _ in range(int(times)):
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