from talon import Context, actions

from ..command import run_simple_command

ctx = Context()
ctx.matches = r"""
tag: browser
app: chrome
app: brave
app: vivaldi
app: microsoft_edge
app: opera
app: safari
app: firefox
"""


@ctx.action_class("browser")
class BrowserActions:
    def go_back():
        run_simple_command("historyGoBack")

    def go_forward():
        run_simple_command("historyGoForward")


@ctx.action_class("user")
class UserActions:
    def tab_duplicate():
        run_simple_command("cloneCurrentTab")
    
    def tab_close_others():
        actions.user.rango_close_other_tabs()
