import os
import os.path
import requests
import time
from talon import ctrl, ui, Module, Context, actions

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

mod = Module()
@mod.action_class
class Actions:
    def idea(commands: str):
        """Send a command to Jetbrains product"""
        print("executing jetbrains", commands)
        global extendCommands
        extendCommands = commands
        for cmd in commands.split(","):
            send_idea_command(cmd)
            time.sleep(0.1)