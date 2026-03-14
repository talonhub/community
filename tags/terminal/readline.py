from talon import Context, actions

ctx = Context()
ctx.matches = r"""
tag: user.readline
"""


@ctx.action_class("edit")
class EditActions:
    def delete_line():
        actions.edit.line_end()
        actions.key("ctrl-u")

    def word_left():
        actions.key("alt-b")

    def word_right():
        actions.key("alt-f")

    def line_end():
        actions.key("ctrl-e")

    def line_start():
        actions.key("ctrl-a")

    def undo():
        actions.key("ctrl-_")

@ctx.action_class("user")
class Actions:
    def cut_line():
        actions.edit.line_start()
        actions.key("ctrl-k")

    def cut_word_left():
        actions.key("ctrl-w")

    def cut_word_right():
        actions.key("alt-d")

    def copy_word_left():
        actions.user.cut_word_left()
        actions.key("ctrl-y")

    def copy_word_right():
        actions.user.cut_word_right()
        actions.key("ctrl-y")
