import appscript
from talon import Context, Module, actions, app, clip, ctrl, storage

ctx = Context()
mod = Module()


@mod.action_class
class Actions:
    def password_open_search():
        """Uses chrome extension to open quick search in extension menu"""
        actions.sleep("100ms")
        actions.key("cmd-shift-x")
        actions.sleep("1000ms")

    def password_search_string(key: str):
        """Uses chrome extension to quick search"""
        actions.sleep("50ms")
        actions.insert(key)
        actions.sleep("500ms")

    def password_copy_password():
        """Uses chrome extension to copy password"""
        actions.sleep("50ms")
        actions.key("right")
        actions.key("down")
        actions.sleep("500ms")
        actions.key("enter")
        actions.sleep("50ms")

    def get_password(key: str):
        """Uses chrome extension to get the password after searching for the supplied key"""
        actions.user.switcher_focus("chrome")
        actions.sleep("500ms")
        actions.user.password_open_search()
        actions.user.password_search_string(key)
        actions.user.password_copy_password()
        actions.sleep("500ms")
        actions.key("esc")
        return clip.get()
