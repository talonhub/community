from talon import Context, Module, actions, settings

"""
Kitty is a terminal emulator for Unix systems (including WSL, unofficially).
Learn more at https://sw.kovidgoyal.net.

The bindings set here assume that your kitty.conf doesn't deviate too far from
the default keybindings.
"""

mod = Module()
mod.setting(
    "kitty_terminal_mod",
    type=str,
    default="ctrl-shift",
    desc="Should match `kitty_mod` in your kitty.conf.",
)
mod.apps.kitty = r"""
app.exe: kitty
app.name: kitty
"""

ctx = Context()
ctx.matches = r"""
app: kitty
"""
ctx.tags = [
    "terminal",
    "user.tabs",
    "user.splits",
    "user.readline",
    "user.generic_unix_shell",
    "user.git",
]


def KITTY_MOD():
    """Fetch the user's configured `kitty_terminal_mod`, if set.

    Override this in your own settings:
        -
        settings():
            user.kitty_terminal_mod = <combo that matches your kitty.conf>

    This has to be a function to defer fetching the value until it's definitely
    been read by Talon.
    """
    return settings.get("user.kitty_terminal_mod")


@ctx.action_class("user")
class UserActions:
    # Override user.splits
    def split_window():
        # actions.key("ctrl-shift-enter")
        actions.key(f"{KITTY_MOD()}-enter")

    def split_next():
        actions.key(f"{KITTY_MOD()}-]")

    def split_last():
        actions.key(f"{KITTY_MOD()}-[")


@ctx.action_class("app")
class AppActions:
    # Override app.tabs
    def tab_open():
        actions.key(f"{KITTY_MOD()}-t")

    def tab_previous():
        actions.key(f"{KITTY_MOD()}-tab")

    def tab_next():
        actions.key("ctrl-tab")

    def tab_close():
        actions.key(f"{KITTY_MOD()}-w")

    # global (overwrite linux/app.py)
    # N.B. that in Kitty's docs, a "window" is a split unless specifically
    # described as an "OS Window." This command opens a new OS window.
    # Use "split window" to get a non-OS window.
    # Also note that your kitty.conf controls whether the new window is in
    # its own process or is owned by the same process as the existing window.
    def window_open():
        actions.key(f"{KITTY_MOD()}-n")


# global (overwrite linux/edit.py)
@ctx.action_class("edit")
class EditActions:
    def page_down():
        actions.key(f"{KITTY_MOD()}-pagedown")

    def page_up():
        actions.key(f"{KITTY_MOD()}-pageup")

    def paste():
        actions.key(f"{KITTY_MOD()}-v")

    def copy():
        actions.key(f"{KITTY_MOD()}-c")

    # Opens the history kitten and assumes that the pager is `less` to initiate
    # a backwards search for the given text. If no text is given, only open the
    # kitten and pager.
    def find(text: str = None):
        actions.key(f"{KITTY_MOD()}-h")
        if text:
            actions.key("?")
            actions.insert(text)
