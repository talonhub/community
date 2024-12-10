from talon import Module, Context
import subprocess

mod = Module()
ctx = Context()

@mod.action_class
class Actions:
    def bluetooth_connect(MAC: str):
        """Connects to a device based on MAC address"""
        subprocess.run(["/opt/homebrew/bin/blueutil", "--connect", MAC])

    def bluetooth_disconnect(MAC: str):
        """Connects to a device based on MAC address"""
        subprocess.run(["/opt/homebrew/bin/blueutil", "--disconnect", MAC])