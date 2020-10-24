import time
from talon import ctrl, ui, Module, Context, actions, clip, app

mod = Module()

ctx = Context()
ctx.matches = r"""
app: Spark
"""


@mod.action_class
class Actions:
    def add_to_do():
        """add email to do app"""
        actions.key("alt-shift-cmd-t")
        actions.key("cmd-enter")
        time.sleep(3)

        actions.key("ctrl-cmd-a")
        actions.key("down")
