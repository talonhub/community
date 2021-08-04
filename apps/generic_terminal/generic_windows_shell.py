from talon import app, Module, Context, actions, ui, imgui, settings, app, registry

mod = Module()
mod.tag("generic_unix_shell")


@mod.action_class
class Actions:
    # implements the function from generic_terminal.talon for unix shells

    def terminal_list_directories():
        """Lists directories"""
        actions.insert("ls")
        actions.key("enter")
        
    def terminal_list_all_directories():
        """Lists all directories including hidden"""
        actions.insert("ls -force")
        actions.key("enter")

    def terminal_change_directory(path: str):
        """Lists change directory"""
        actions.insert("cd {}".format(path))
        if path:
            actions.key("enter")

    def terminal_change_directory_root():
        """Root of current drive"""
        actions.insert("cd /")
        actions.key("enter")

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
