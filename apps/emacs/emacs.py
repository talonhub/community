from talon import Context, Module, actions

mod = Module()
ctx = Context()
ctx.matches = r'''
app: Emacs
app: emacs
'''

@mod.action_class
class Actions:
    def emacs_command(name: str): "Runs an emacs command."
    def emacs_prefix(n: int): "Inputs a prefix argument."
    def emacs_help(key: str = None): "Runs the emacs help command prefix."

@ctx.action_class('user')
class UserActions:
    def split_window():               actions.key('ctrl-x 2')
    def split_window_vertically():    actions.key('ctrl-x 2')
    def split_window_horizontally():  actions.key('ctrl-x 3')
    def split_next():                 actions.key("ctrl-'")
    def split_last():                 actions.key("alt-ctrl-'")
    def split_clear():                actions.key('ctrl-x 0')
    def split_clear_all():            actions.key('ctrl-x 1')

    def emacs_command(name):
        actions.key("alt-x")
        actions.insert(name)
        actions.key("enter")

    # Applying meta to each key is fewer keypresses overall and works in
    # ansi-term mode.
    def emacs_prefix(n): actions.key(" ".join(f"alt-{i}" for i in str(n)))
    #def emacs_prefix(n): actions.key(f'ctrl-u {" ".join(str(n))}')

    # NB. f1 works in ansi-term mode; C-h doesn't.
    def emacs_help(key = None):
        actions.key("f1")
        if key is not None: actions.key(key)

    def dictation_peek_left():
        # space-backspace clobbers transient selection if it exists; otherwise
        # if there's a transient selection we won't overwrite it.
        actions.key("space backspace")
        actions.key("ctrl-@")
        actions.edit.word_left()
        text = actions.edit.selected_text()
        actions.key("ctrl-u ctrl-@")
        return text
 
    def dictation_peek_right():
        actions.edit.extend_line_end()
        text = actions.edit.selected_text()
        actions.key("ctrl-u ctrl-@")
        return text

    def select_range(line_start, line_end):
        actions.edit.jump_line(line_start)
        actions.key("ctrl-@ ctrl-@")
        actions.edit.jump_line(line_end)
        actions.edit.line_end()
        actions.edit.right()

@ctx.action_class('edit')
class EditActions:
    def save():       actions.key('ctrl-x ctrl-s')
    def copy():       actions.key('alt-w')
    def cut():        actions.key('ctrl-w')
    def undo():       actions.key('ctrl-_')
    def paste():      actions.key('ctrl-y')

    def word_left():         actions.key('alt-b')
    def word_right():        actions.key('alt-f')
    def extend_word_left():  actions.key('shift-alt-b')
    def extend_word_right(): actions.key('shift-alt-f')
    def select_all():        actions.key('ctrl-x h ctrl-u ctrl-x ctrl-x')

    def line_swap_down():    actions.key('down ctrl-x ctrl-t up')
    def line_swap_up():      actions.key('ctrl-x ctrl-t up:2')
    def line_clone():        actions.key('ctrl-a ctrl-k ctrl-y enter ctrl-y home')
    def jump_line(n):
        actions.user.emacs_prefix(n)
        actions.key("alt-g g")
    def select_line(n: int = None):
        if n is not None: actions.edit.jump_line(n)
        actions.key("ctrl-a shift-down")

    def indent_more():
        actions.user.emacs_prefix(4)
        actions.key('ctrl-x tab')
    def indent_less():
        actions.user.emacs_prefix(-4)
        actions.key('ctrl-x tab')

    def zoom_in():    actions.key('ctrl-x ctrl-+')
    def zoom_out():   actions.key('ctrl-x ctrl--')
    def zoom_reset(): actions.key('ctrl-x ctrl-0')

    def find(text: str = None):
        actions.key("ctrl-s")
        if text: actions.insert(text)
    def find_next(): actions.key('ctrl-s')
    def find_previous(): actions.key('ctrl-r')

    ## This causes delete_line to entirely delete white space lines, which is
    ## less predictable. :/
    def delete_line(): actions.key("ctrl-a ctrl-k")

@ctx.action_class('code')
class CodeActions:
    def toggle_comment(): actions.user.emacs_command('comment-dwim')
    def language():
        if "*scratch*" == actions.win.filename(): return "elisp"
        return actions.next()

@ctx.action_class('app')
class AppActions:
    def tab_next():     actions.key("ctrl-'")
    def tab_previous(): actions.key("alt-ctrl-'")
    def tab_close():    actions.key('ctrl-x 0')
    def tab_reopen():   actions.key('ctrl-x 4 b enter')
    def tab_open():     actions.key('ctrl-x 2')
    def window_open():  actions.key('ctrl-x 5 2')

@ctx.action_class('win')
class WinActions:
    # This assumes the title is/contains the filename.
    # To do this, put this in init.el:
    # (setq-default frame-title-format '((:eval (buffer-name (window-buffer (minibuffer-selected-window))))))
    def filename(): return actions.win.title()
