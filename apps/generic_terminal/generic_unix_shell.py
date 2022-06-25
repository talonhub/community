from talon import Context, Module, actions

ctx = Context()
mod = Module()
ctx.matches = r"""
tag: user.generic_unix_shell
"""


@ctx.action_class("user")
class Actions:
    # implements the function from generic_terminal.talon for unix shells

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

@ctx.action_class("edit")
class EditActions:
    def delete_line():
        actions.edit.line_start()
        actions.key("ctrl-k")

    def delete_word():
        actions.key("alt-d")

    def line_end():
        actions.key("ctrl-a")

    def page_down():
        actions.key("shift-pagedown")

    def page_up():
        actions.key("shift-pageup")

    def redo():
        actions.insert("up")

    def undo():
        actions.insert("up")
    
    def word_left():
        actions.key("alt-b")

    def word_right():
        actions.key("alt-f")

@ctx.action_class("user")
class UserEditActions:
    def delete_word_left():
        actions.key("ctrl-w")
        
    def delete_word_right():
        actions.edit.word_right()
        actions.edit.delete_word_left()
