import time

from talon import Module, actions, settings

mod = Module()
mod.list("vimvixen", desc="Common vimvixen")
mod.setting(
    "vimvixen_auto_focus",
    type=int,
    default=0,
    desc="Always attempt to focus vimvixen in a way from search, URL bar, etc",
)


class VimVixen:
    def focus():
        """
        Implement a trick to cause vimvixen to focus correctly. This allows us
        to run certain commands that wouldn't normally work, for instance if
        you were already in the search bar, or the url bar, etc.
        """
        # highlight URL bar
        actions.key("ctrl-l")
        time.sleep(0.01)
        # pop keyboard
        actions.key("escape")
        # trigger find (won't work unless we were in URL bar
        actions.key("ctrl-f")
        time.sleep(0.01)
        # escape out of find window
        actions.key("escape")
        actions.key("escape")
        # now have general focus


@mod.action_class
class Actions:
    def vimvixen_focus():
        "Expose VimVixen class method"
        VimVixen.focus()

    def vimvixen_key(key: str):
        "Regular talon key() prefixed with an optional focus."
        if settings.get("user.vimvixen_auto_focus") >= 1:
            VimVixen.focus()
        actions.key(key)

    def vimvixen_insert(text: str):
        "Regular talon insert() prefixed with an optional focus."
        if settings.get("user.vimvixen_auto_focus") >= 1:
            VimVixen.focus()
        actions.insert(text)
