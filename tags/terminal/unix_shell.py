from talon import Context, Module, actions

ctx = Context()
mod = Module()
ctx.matches = r"""
tag: user.generic_unix_shell
"""

# Uncomment the following line to enable common unix utilities from unix_utilities.py
# ctx.tags = ["user.unix_utilities"]

# If your terminal is a bash or zsh, set tag user.generic_unix_shell to enable
# additional capabilities.


@ctx.action_class("user")
class Actions:
    # Implements the functions from terminal.py for unix shells

    def terminal_list_directories():
        """Lists directories"""
        actions.insert("ls")
        actions.key("enter")

    def terminal_list_all_directories():
        """Lists all directories including hidden"""
        actions.insert("ls -a")
        actions.key("enter")

    def terminal_change_directory(path: str):
        """Lists change directory"""
        actions.insert(f"cd {path}")
        if path:
            actions.key("enter")

    def terminal_change_directory_root():
        """Root of current drive"""
        actions.insert("cd /")
        actions.key("enter")

    def terminal_change_directory_toggle():
        """Toggle traversal between the two most recent directories"""
        actions.insert("cd -")
        actions.key("enter")

    def terminal_change_directory_up(count: int):
        """Traverse a given number of directories upwards"""
        actions.insert("cd " + "/".join(count * [".."]))

    def terminal_clear_screen():
        """Clear screen"""
        actions.insert("clear")
        actions.key("enter")

    def terminal_run_last():
        """Repeats the last command"""
        actions.key("up enter")

    def terminal_rerun_search(command: str):
        """Searches through the previously executed commands"""
        actions.key("ctrl-r")
        actions.insert(command)

    def terminal_kill_all():
        """kills the running command"""
        actions.key("ctrl-c")
        actions.insert("y")
        actions.key("enter")


mod.tag("generic_unix_shell_bash", "tag to enable bash capabilities in unix shells")
bash_ctx = Context()
bash_ctx.matches = r"""
tag: user.generic_unix_shell
and tag: user.generic_unix_shell_bash
"""


@bash_ctx.action_class("user")
class BashActions:
    def terminal_change_directory_back():
        """Traverse back to the previous directory on the directory stack"""
        # This is only possible on bash shells (or zsh etc.), but not on POSIX shells.
        actions.insert("popd")
        actions.key("enter")
