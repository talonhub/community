from talon import Context, Module, actions, app

ctx = Context()
mod = Module()

mod.apps.brave = "app.name: Brave Browser"
# TODO: Add other OS application identifiers
mod.apps.brave = """
os: mac
and app.bundle: com.brave.Browser
"""
ctx.matches = r"""
app: brave
"""


@ctx.action_class("user")
class user_actions:
    def tab_jump(number: int):
        if number < 9:
            if app.platform == "mac":
                actions.key(f"cmd-{number}")
            else:
                actions.key(f"ctrl-{number}")

    def tab_final():
        if app.platform == "mac":
            actions.key("cmd-9")
        else:
            actions.key("ctrl-9")

    def tab_close_wrapper():
        actions.sleep("180ms")
        actions.app.tab_close()

    def tab_duplicate():
        """Limitation: this will not work if the text in your address bar has been manually edited.
        Long-term we want a better shortcut from browsers.
        """
        actions.browser.focus_address()
        actions.sleep("180ms")
        actions.key("alt-enter")


@ctx.action_class("browser")
class browser_actions:
    def go(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        actions.key("enter")
