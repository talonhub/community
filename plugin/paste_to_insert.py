import logging

from talon import Context, Module, actions

mod = Module()
ctx = Context()

paste_to_insert_threshold_setting = mod.setting(
    "paste_to_insert_threshold",
    type=int,
    default=-1,
    desc="""Use paste to insert text longer than this many characters.
Zero means always paste; -1 means never paste.
""",
)


@ctx.action_class("main")
class MainActions:
    def insert(text):
        threshold = paste_to_insert_threshold_setting.get()
        if 0 <= threshold < len(text):
            actions.user.paste(text)
            return
        actions.next(text)
