# defines the default edit actions for linux

from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: linux
"""


@ctx.action_class("edit")
class EditActions:
    def copy():
        actions.key("ctrl-c")

    def cut():
        actions.key("ctrl-x")

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
        actions.key("shift-ctrl-end")

    def extend_file_start():
        actions.key("shift-ctrl-home")

    def extend_left():
        actions.key("shift-left")
        # action(edit.extend_line):

    def extend_line_down():
        actions.key("shift-down")

    def extend_line_end():
        actions.key("shift-end")

    def extend_line_start():
        actions.key("shift-home")

    def extend_line_up():
        actions.key("shift-up")

    def extend_page_down():
        actions.key("shift-pagedown")

    def extend_page_up():
        actions.key("shift-pageup")
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
        actions.key("ctrl-shift-left")

    def extend_word_right():
        actions.key("ctrl-shift-right")

    def file_end():
        actions.key("ctrl-end")

    def file_start():
        actions.key("ctrl-home")

    def find(text: str = None):
        actions.key("ctrl-f")
        if text:
            actions.insert(text)

    def find_previous():
        actions.key("shift-f3")

    def find_next():
        actions.key("f3")

    def indent_less():
        actions.key("home delete")

    def indent_more():
        actions.key("home tab")
        # action(edit.jump_column(n: int)
        # action(edit.jump_line(n: int)

    def left():
        actions.key("left")

    def line_down():
        actions.key("down home")

    def line_end():
        actions.key("end")

    def line_insert_up():
        actions.key("home enter up")

    def line_start():
        actions.key("home")

    def line_up():
        actions.key("up home")
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
        actions.key("ctrl-v")
        # action(paste_match_style):

    def print():
        actions.key("ctrl-p")

    def redo():
        actions.key("ctrl-y")

    def right():
        actions.key("right")

    def save():
        actions.key("ctrl-s")

    def save_all():
        actions.key("ctrl-shift-s")

    def select_all():
        actions.key("ctrl-a")

    def select_line(n: int = None):
        if n is not None:
            actions.edit.jump_line(n)
        actions.key("end shift-home")
        # action(edit.select_lines(a: int, b: int)):

    def select_none():
        actions.key("right")
        # action(edit.select_paragraph):
        # action(edit.select_sentence):

    def undo():
        actions.key("ctrl-z")

    def up():
        actions.key("up")

    def word_left():
        actions.key("ctrl-left")

    def word_right():
        actions.key("ctrl-right")

    def zoom_in():
        actions.key("ctrl-+")

    def zoom_out():
        actions.key("ctrl--")

    def zoom_reset():
        actions.key("ctrl-0")
