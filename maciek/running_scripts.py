import os
import subprocess

from talon import Module

mod = Module()


@mod.action_class
class Actions:
    def run_in_fish_shell(cmd: str):
        """execute a command on the system without blocking"""
        print(100 * "=")
        print(cmd)
        subprocess.Popen(["/opt/homebrew/bin/fish", "-c", cmd])
