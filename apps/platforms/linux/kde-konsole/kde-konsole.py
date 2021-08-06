from talon import Context, Module, actions

import os

ctx = Context()
mod = Module()
ctx.matches = r"""
app.name: konsole
"""

@ctx.action_class("user")
class user_actions:

    # tabs-tag functions implementations
    def tab_jump(number):
        actions.key("alt-{}".format(number))

    # tab_final is not supported by konsole by default
    # but short cut can be configured

@ctx.action_class("app")
class app_actions:
    # tabs-tag functions implementations
    def tab_open():
        actions.key("ctrl-shift-t")

    def tab_previous():
        actions.key("shift-left")

    def tab_next():
        actions.key("shift-right")

    def tab_close():
        actions.key("ctrl-shift-w")

    # tab_reopen is not supported by konsole

    def window_open():
        actions.key('ctrl-shift-n')

