from talon import Context, Module, actions

ctx = Context()
mod = Module()

apps = mod.apps
apps.gdocs = """
tag: browser
browser.host: docs.google.com
"""

@ctx.action_class("user")
class FindAndReplace:
    """ Override generic find-and-replace """
    def find(text: str):
        actions.key("cmd-f")
        actions.insert(text)

    def find_next():
        actions.key("cmd-g")

    def find_previous():
        actions.key("cmd-shift-g")

    def replace(text: str):
        actions.key("cmd-shift-h")
        actions.insert(text)


@ctx.action_class("edit")
class EditActions:
    def paste_match_style():
        actions.key("cmd-shift-v")