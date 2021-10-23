from talon import Context, actions, ui, Module, app


mod = Module()
mod.apps.broot = """
os: mac
and app: kitty
and win.title: /br/
"""


@mod.action_class
class Actions:
    def broot_quit():
        """This description is mandatory"""
