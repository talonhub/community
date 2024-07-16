from talon import Context, Module, actions

mod = Module()
mod.tag("navigation")

ctx_browser = Context()
ctx_browser.matches = r"""
tag: browser
"""

ctx_mac = Context()
ctx_mac.matches = r"""
os: mac
"""


@ctx_browser.action_class("user")
class BrowserActions:
    def go_back():
        actions.browser.go_back()

    def go_forward():
        actions.browser.go_forward()


@ctx_mac.action_class("user")
class MacActions:
    def go_back():
        actions.key("cmd-]")

    def go_forward():
        actions.key("cmd-[")


@mod.action_class
class Actions:
    def go_back():
        """Navigate back"""
        actions.key("alt-left")

    def go_forward():
        """Navigate forward"""
        actions.key("alt-right")
