from talon import Context, Module, actions

import os

ctx = Context()
mod = Module()
ctx.matches = r"""
app.name: konsole
"""

@ctx.action_class("user")
class user_actions:
    # terminal-tag functions implementation
    def terminal_list_directories():
        actions.insert("ls")
        actions.key("enter")

    def terminal_list_all_directories():
        actions.insert("ls -a")
        actions.key("enter")

    def terminal_change_directory(path: str):
        actions.insert("cd {}".format(path))
        if path:
            actions.key("enter")

    def terminal_change_directory_root():
        actions.insert("cd /")
        actions.key("enter")

    def terminal_clear_screen():
        actions.insert("clear")
        actions.key("enter")

    def terminal_run_last():
        actions.key("up enter")

    def terminal_kill_all():
        actions.key("ctrl-c")
        actions.insert("y")
        actions.key("enter")

    def terminal_rerun_search(command: str):
        actions.key("ctrl-r")
        actions.insert(command)


    # tabs-tag functions implementations
    def tab_jump(number):
        actions.key("alt-{}".format(number))

    # tab_final is not supported by konsole by default
    # but short cut can be configured

@ctx.action_class("app")
class app_actions:
    # tabs-tag functions implementations
    def tab_open():
        actions.key("ctrl-shift-t")

    def tab_previous():
        actions.key("shift-left")

    def tab_next():
        actions.key("shift-right")

    def tab_close():
        actions.key("ctrl-shift-w")

    # tab_reopen is not supported by konsole

