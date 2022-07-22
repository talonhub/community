from talon import Context, Module, actions
import logging

mod = Module()
setting_meta = mod.setting(
    'emacs_meta',
    type=str,
    default='esc',
    desc="""What to use for the meta key in emacs. Defaults to 'esc', since that should work everywhere. Other options are 'alt' and 'cmd'.""",
)

ctx = Context()
ctx.matches = r'''
app: Emacs
app: emacs
'''

def meta(keys):
    m = setting_meta.get()
    if m == 'alt': return ' '.join('alt-' + k for k in keys.split())
    elif m == 'cmd': return ' '.join('cmd-' + k for k in keys.split())
    elif m != 'esc':
        logging.error(f"Unrecognized 'emacs_meta' setting: {m!r}. Falling back to 'esc'.")
    return 'esc ' + keys

@mod.action_class
class Actions:
    def emacs_meta(key: str):
        "Presses some keys modified by Emacs' meta key."
        actions.key(meta(key))

    def emacs_command(name: str):
        "Runs an emacs command."
        actions.user.emacs_meta("x")
        actions.insert(name)
        actions.key("enter")

    def emacs_prefix(n: int):
        "Inputs a numeric prefix argument."
        # Applying meta to each key may be fewer keypresses overall and 'works'
        # in ansi-term mode.
        actions.user.emacs_meta(' '.join(str(n)))
        # actions.key(f'ctrl-u {" ".join(str(n))}') # Alternative using ctrl-u.

    def emacs_help(key: str = None):
        "Runs the emacs help command prefix, optionally followed by some keys."
        # NB. f1 works in ansi-term mode; C-h doesn't.
        actions.key("f1")
        if key is not None: actions.key(key)

@ctx.action_class('user')
class UserActions:
    def split_window():               actions.key('ctrl-x 2')
    def split_window_vertically():    actions.key('ctrl-x 2')
    def split_window_up():            actions.key('ctrl-x 2')
    def split_window_down():          actions.key('ctrl-x 2 ctrl-x o')
    def split_window_horizontally():  actions.key('ctrl-x 3')
    def split_window_left():          actions.key('ctrl-x 3')
    def split_window_right():         actions.key('ctrl-x 3 ctrl-x o')
    def split_clear():                actions.key('ctrl-x 0')
    def split_clear_all():            actions.key('ctrl-x 1')
    # def split_maximize():             actions.key('ctrl-x 1')
    def split_reset():                actions.key('ctrl-x +')
    def split_next():                 actions.key("ctrl-x o")
    def split_last():
        actions.user.emacs_prefix(-1)
        actions.key("ctrl-x o")
    def split_flip():
        actions.key('ctrl-x b enter ctrl-x o ctrl-x b enter')
        actions.user.split_last()
        actions.key('ctrl-x b enter ctrl-x o')

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
    def save_all():   actions.key('ctrl-x s') # not quite right
    def copy():       actions.user.emacs_meta('w')
    def cut():        actions.key('ctrl-w')
    def undo():       actions.key('ctrl-_')
    def paste():      actions.key('ctrl-y')
    def select_all(): actions.key('ctrl-x h ctrl-u ctrl-x ctrl-x')

    def word_left():         actions.user.emacs_meta('b')
    def word_right():        actions.user.emacs_meta('f')
    def extend_word_left():  actions.user.emacs_meta('shift-b')
    def extend_word_right(): actions.user.emacs_meta('shift-f')
    def sentence_start(): actions.user.emacs_meta('a')
    def sentence_end(): actions.user.emacs_meta('e')
    def extend_sentence_start(): actions.user.emacs_meta('shift-a')
    def extend_sentence_end(): actions.user.emacs_meta('shift-e')
    def paragraph_start(): actions.user.emacs_meta('{')
    def paragraph_end(): actions.user.emacs_meta('}')

    def line_swap_down():    actions.key('down ctrl-x ctrl-t up')
    def line_swap_up():      actions.key('ctrl-x ctrl-t up:2')
    def line_clone():        actions.key('ctrl-a ctrl-k ctrl-y enter ctrl-y home')
    def delete_line():       actions.key("ctrl-a ctrl-k")
    def jump_line(n):
        actions.user.emacs_prefix(n)
        actions.user.emacs_meta('g')
        actions.key('g')

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

@ctx.action_class('code')
class CodeActions:
    def toggle_comment(): actions.user.emacs_command('comment-dwim')
    def language():
        # Assumes win.filename() gives buffer name.
        if "*scratch*" == actions.win.filename(): return "elisp"
        return actions.next()

@ctx.action_class('app')
class AppActions:
    def tab_next():     actions.user.split_next()
    def tab_previous(): actions.user.split_last()
    def tab_close():    actions.user.split_clear()
    def tab_reopen():   actions.key('ctrl-x 4 b enter')
    def tab_open():     actions.key('ctrl-x 2 ctrl-x o')
    def window_open():  actions.key('ctrl-x 5 2')

@ctx.action_class('win')
class WinActions:
    # This assumes the title is/contains the filename.
    # To do this, put this in init.el:
    # (setq-default frame-title-format '((:eval (buffer-name (window-buffer (minibuffer-selected-window))))))
    def filename(): return actions.win.title()
