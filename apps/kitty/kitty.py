from talon import Context, Module, actions

mod = Module()
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


# Change this to match `kitty_mod` in your kitty.conf.
KITTY_MOD = "ctrl-shift"
# Note that not all commands use `kitty_mod`. Be sure to review the bindings
# set here if you've made extensive changes to kitty's default keybinds.


@ctx.action_class("user")
class UserActions:
    # Override user.splits
    def split_window():
        # actions.key("ctrl-shift-enter")
        actions.key(f"{KITTY_MOD}-enter")

    def split_next():
        actions.key(f"{KITTY_MOD}-]")

    def split_last():
        actions.key(f"{KITTY_MOD}-[")


@ctx.action_class("app")
class AppActions:
    # Override app.tabs
    def tab_open():
        actions.key(f"{KITTY_MOD}-t")

    def tab_previous():
        actions.key(f"{KITTY_MOD}-tab")

    def tab_next():
        actions.key("ctrl-tab")

    def tab_close():
        actions.key(f"{KITTY_MOD}-w")

    # global (overwrite linux/app.py)
    # N.B. that in Kitty's docs, a "window" is a split unless specifically
    # described as an "OS Window." This command opens a new OS window.
    # Use "split window" to get a non-OS window.
    # Also note that your kitty.conf controls whether the new window is in
    # its own process or is owned by the same process as the existing window.
    def window_open():
        actions.key(f"{KITTY_MOD}-n")


# global (overwrite linux/edit.py)
@ctx.action_class("edit")
class EditActions:
    def page_down():
        actions.key(f"{KITTY_MOD}-pagedown")

    def page_up():
        actions.key(f"{KITTY_MOD}-pageup")

    def paste():
        actions.key(f"{KITTY_MOD}-v")

    def copy():
        actions.key(f"{KITTY_MOD}-c")

    # Opens the history kitten and assumes that the pager is `less` to initiate
    # a backwards search for the given text. If no text is given, only open the
    # kitten and pager.
    def find(text: str = None):
        actions.key(f"{KITTY_MOD}-h")
        if text:
            actions.key("?")
            actions.insert(text)
