from talon import Context, Module, actions

ctx = Context()
mod = Module()

ctx.matches = r"""
tag: user.tmux
"""

setting_tmux_prefix_key = mod.setting(
    "tmux_prefix_key",
    type=str,
    default="b",
    desc="The key used to prefix all tmux commands",
)


@mod.action_class
class TmuxActions:
    def do_tmux_prefix():
        """press control and the configured tmux prefix key"""
        actions.key(f"ctrl-{setting_tmux_prefix_key.get()}")

    def do_tmux_keybind(key: str):
        """press tmux prefix followed by a key bind"""
        actions.user.do_tmux_prefix()
        actions.key(key)

    def enter_tmux_command_mode():
        """enter tmux command mode by using prefix and : key"""
        actions.user.do_tmux_keybind(":")

    def enter_tmux_command(command: str):
        """enter tmux command without executing, for safety on destructive commands"""
        actions.user.enter_tmux_command_mode()
        actions.insert(command)

    def execute_tmux_command(command: str):
        """execute tmux command"""
        actions.user.enter_tmux_command(command)
        actions.key("enter")
        actions.sleep("100ms")

    def execute_tmux_command_with_confirmation(command: str, confirmation_prompt: str):
        """execute tmux command with confirm-before"""
        actions.user.execute_tmux_command(
            f'confirm-before -p "{confirmation_prompt} (y/n)" {command}'
        )
        actions.key("\n")


@ctx.action_class("app")
class AppActions:
    def tab_open():
        actions.user.execute_tmux_command("new-window")

    def tab_next():
        actions.user.execute_tmux_command("select-window -n")

    def tab_previous():
        actions.user.execute_tmux_command("select-window -p")


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        actions.user.execute_tmux_command(f"select-window -t {number}")

    def tab_close_wrapper():
        actions.user.execute_tmux_command_with_confirmation(
            "kill-window", "kill-window #W?"
        )

    def split_window_right():
        actions.user.split_window_horizontally()
        actions.user.execute_tmux_command("swap-pane -U -s #P")

    def split_window_left():
        actions.user.split_window_horizontally()

    def split_window_down():
        actions.user.split_window_vertically()
        actions.user.execute_tmux_command("swap-pane -U -s #P")

    def split_window_up():
        actions.user.split_window_vertically()

    def split_flip():
        actions.user.execute_tmux_command("next-layout")

    def split_window_vertically():
        actions.user.execute_tmux_command("split-pane")

    def split_window_horizontally():
        actions.user.execute_tmux_command("split-pane -h")

    def split_maximize():
        """toggle the maximization because zooming when already zoomed is pointless"""
        actions.user.execute_tmux_command("resize-pane -Z")

    def split_reset():
        actions.user.execute_tmux_command("resize-pane -Z")

    def split_window():
        actions.user.split_window_horizontally()

    def split_clear():
        actions.user.execute_tmux_command_with_confirmation(
            "kill-pane", "kill-pane #P?"
        )

    def split_next():
        """select-pane doesn't seem to support the prefix-o behavior"""
        actions.user.do_tmux_keybind("o")

    def split_last():
        actions.user.execute_tmux_command("select-pane -l")

    def split_number(index: int):
        actions.user.execute_tmux_command(f"select-pane -t {index}")
