from talon import Context, actions, ui, Module, app

mod = Module()


@mod.action_class("fzf")
class fzf:
    def delete_big_word():
        actions.edit.word_right()
        actions.key("ctrl-shift-w")
