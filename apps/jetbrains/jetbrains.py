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
    "com.jetbrains.rubymine-EAP": 8661,
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
    "jetbrains-rubymine-eap": 8661,
    "jetbrains-studio": 8652,
    "jetbrains-webstorm": 8663,
    "RubyMine": 8661,
    "RubyMine-EAP": 8661,
    "PyCharm": 8658,
    "pycharm64.exe": 8658,
    "webstorm64.exe": 8663,
}


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

mod.apps.jetbrains = "app.name: /jetbrains/"
mod.apps.jetbrains = "app.name: IntelliJ IDEA"
mod.apps.jetbrains = "app.name: PyCharm"
mod.apps.jetbrains = "app.name: RubyMine"
mod.apps.jetbrains = "app.name: RubyMine-EAP"

# windows
mod.apps.jetbrains = "app.name: idea64.exe"
mod.apps.jetbrains = "app.name: PyCharm64.exe"
mod.apps.jetbrains = "app.name: pycharm64.exe"
mod.apps.jetbrains = "app.name: webstorm64.exe"
mod.apps.jetbrains = """
os: mac
and app.bundle: com.jetbrains.pycharm
"""


@mod.action_class
class Actions:
    def idea(commands: str):
        """Send a command to Jetbrains product"""
        idea_commands(commands)

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


ctx.matches = r"""
app: jetbrains
"""


@ctx.action_class("win")
class win_actions:
    def file_ext():
        return actions.win.title().split(".")[-1]


@ctx.action_class("edit")
class edit_actions:
    def jump_line(n: int):
        actions.user.idea("goto {} 0".format(n))
        # move the cursor to the first nonwhite space character of the line
        actions.user.idea("action EditorLineEnd")
        actions.user.idea("action EditorLineStart")


@ctx.action_class("user")
class user_actions:
    def tab_jump(number: int):
        # depends on plugin GoToTabs
        if number < 10:
            actions.user.idea("action GoToTab{}".format(number))

    def extend_until_line(line: int):
        actions.user.idea("extend {}".format(line))

    def select_range(line_start: int, line_end: int):
        # if it's a single line, select the entire thing including the ending new-line5
        if line_start == line_end:
            actions.user.idea("goto {} 0".format(line_start))
            actions.user.idea("action EditorSelectLine"),
        else:
            actions.user.idea("range {} {}".format(line_start, line_end))

    def extend_camel_left():
        actions.user.idea("action EditorPreviousWordInDifferentHumpsModeWithSelection")

    def extend_camel_right():
        actions.user.idea("action EditorNextWordInDifferentHumpsModeWithSelection")

    def camel_left():
        actions.user.idea("action EditorPreviousWordInDifferentHumpsMode")

    def camel_right():
        actions.user.idea("action EditorNextWordInDifferentHumpsMode")

    def line_clone(line: int):
        actions.user.idea("clone {}".format(line))
