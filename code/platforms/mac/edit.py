from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
"""


@ctx.action_class("edit")
class EditActions:
    def copy():
        actions.key("cmd-c")

    def cut():
        actions.key("cmd-x")

    def delete():
        actions.key("backspace")

    def delete_line():
        actions.edit.select_line()
        actions.edit.delete()
        # action(edit.delete_paragraph):
        # action(edit.delete_sentence):

    def delete_word():
        actions.edit.select_word()
        actions.edit.delete()

    def down():
        actions.key("down")
        # action(edit.extend_again):
        # action(edit.extend_column):

    def extend_down():
        actions.key("shift-down")

    def extend_file_end():
        actions.key("cmd-shift-down")

    def extend_file_start():
        actions.key("cmd-shift-up")

    def extend_left():
        actions.key("shift-left")
        # action(edit.extend_line):

    def extend_line_down():
        actions.key("shift-down")

    def extend_line_end():
        actions.key("cmd-shift-right")

    def extend_line_start():
        actions.key("cmd-shift-left")

    def extend_line_up():
        actions.key("shift-up")

    def extend_page_down():
        actions.key("cmd-shift-pagedown")

    def extend_page_up():
        actions.key("cmd-shift-pageup")
        # action(edit.extend_paragraph_end):
        # action(edit.extend_paragraph_next()):
        # action(edit.extend_paragraph_previous()):
        # action(edit.extend_paragraph_start()):

    def extend_right():
        actions.key("shift-right")
        # action(edit.extend_sentence_end):
        # action(edit.extend_sentence_next):
        # action(edit.extend_sentence_previous):
        # action(edit.extend_sentence_start):

    def extend_up():
        actions.key("shift-up")

    def extend_word_left():
        actions.key("shift-alt-left")

    def extend_word_right():
        actions.key("shift-alt-right")

    def file_end():
        actions.key("cmd-down cmd-left")

    def file_start():
        actions.key("cmd-up cmd-left")

    def find(text: str = None):
        actions.key("cmd-f")
        # actions.insert(text)

    def find_next():
        actions.key("cmd-g")

    def find_previous():
        actions.key("cmd-shift-g")

    def indent_less():
        actions.key("cmd-left delete")

    def indent_more():
        actions.key("cmd-left tab")
        # action(edit.jump_column(n: int)
        # action(edit.jump_line(n: int)

    def left():
        actions.key("left")

    def line_down():
        actions.key("down home")

    def line_end():
        actions.key("cmd-right")

    def line_insert_up():
        actions.key("cmd-left enter up")

    def line_start():
        actions.key("cmd-left")

    def line_up():
        actions.key("up cmd-left")
        # action(edit.move_again):

    def page_down():
        actions.key("pagedown")

    def page_up():
        actions.key("pageup")
        # action(edit.paragraph_end):
        # action(edit.paragraph_next):
        # action(edit.paragraph_previous):
        # action(edit.paragraph_start):

    def paste():
        actions.key("cmd-v")

    def paste_match_style():
        actions.key("cmd-alt-shift-v")

    def print():
        actions.key("cmd-p")

    def redo():
        actions.key("cmd-shift-z")

    def right():
        actions.key("right")

    def save():
        actions.key("cmd-s")

    def save_all():
        actions.key("cmd-shift-s")

    def select_all():
        actions.key("cmd-a")

    def select_line(n: int = None):
        if n is not None:
            actions.edit.jump_line(n)
        actions.key("cmd-right cmd-shift-left")
        # action(edit.select_lines(a: int, b: int)):

    def select_none():
        actions.key("right")
        # action(edit.select_paragraph):
        # action(edit.select_sentence):

    def select_word():
        actions.edit.right()
        actions.edit.word_left()
        actions.edit.extend_word_right()

    def undo():
        actions.key("cmd-z")

    def up():
        actions.key("up")

    def word_left():
        actions.key("alt-left")

    def word_right():
        actions.key("alt-right")

    def zoom_in():
        actions.key("cmd-=")

    def zoom_out():
        actions.key("cmd--")

    def zoom_reset():
        actions.key("cmd-0")
