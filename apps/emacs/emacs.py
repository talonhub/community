import logging
from typing import Optional

from talon import Context, Module, actions, settings

mod = Module()
mod.setting(
    "emacs_meta",
    type=str,
    default="esc",
    desc="""What to use for the meta key in emacs. Defaults to 'esc', since that should work everywhere. Other options are 'alt' and 'cmd'.""",
)

mod.apps.emacs = "app.name: Emacs"
mod.apps.emacs = "app.name: emacs"
mod.apps.emacs = "app.name: /^GNU Emacs/"
mod.apps.emacs = """
os: mac
app.bundle: org.gnu.Emacs
"""
mod.apps.emacs = """
os: windows
app.exe: emacs.exe
"""

ctx = Context()
ctx.matches = "app: emacs"


def meta(keys):
    m = settings.get("user.emacs_meta")
    if m == "alt":
        return " ".join("alt-" + k for k in keys.split())
    elif m == "cmd":
        return " ".join("cmd-" + k for k in keys.split())
    elif m != "esc":
        logging.error(
            f"Unrecognized 'emacs_meta' setting: {m!r}. Falling back to 'esc'."
        )
    return "esc " + keys


def meta_fixup(k):
    if k.startswith("meta-"):
        k = meta(k[len("meta-") :])
    elif "meta-" in k:
        raise NotImplementedError("user.emacs_key(): please put meta- first")
    return k


@mod.action_class
class Actions:
    def emacs_meta(key: str):
        "Presses some keys modified by Emacs' meta key."
        actions.key(meta(key))

    def emacs_key(keys: str):
        """
        Presses some keys, translating 'meta-' prefix to the appropriate keys. For
        example, if the setting user.emacs_meta = 'esc', user.emacs_key("meta-ctrl-a")
        becomes key("esc ctrl-a").
        """
        # TODO: handle corner-cases like key(" ") and key("ctrl- "), etc.
        actions.key(" ".join(meta_fixup(k) for k in keys.split()))

    def emacs_prefix(n: Optional[int] = None):
        "Inputs a prefix argument."
        if n is None:
            # `M-x universal-argument` doesn't have the same effect as pressing the key.
            prefix_key = actions.user.emacs_command_keybinding("universal-argument")
            actions.key(prefix_key or "ctrl-u")  # default to ctrl-u
        else:
            # Applying meta to each key can use fewer keypresses and 'works' in ansi-term
            # mode.
            actions.user.emacs_meta(" ".join(str(n)))

    def emacs(command_name: str, prefix: Optional[int] = None):
        """
        Runs the emacs command `command_name`. Defaults to using M-x, but may use
        a key binding if known or rpc if available. Provides numeric prefix argument
        `prefix` if specified.
        """
        meta_x = actions.user.emacs_command_keybinding("execute-extended-command")
        keys = actions.user.emacs_command_keybinding(command_name)
        short_form = actions.user.emacs_command_short_form(command_name)
        if prefix is not None:
            actions.user.emacs_prefix(prefix)
        if keys is not None:
            actions.user.emacs_key(keys)
        else:
            actions.user.emacs_key(meta_x or "meta-x")
            actions.insert(short_form or command_name)
            actions.key("enter")

    def emacs_help(key: str = None):
        "Runs the emacs help command prefix, optionally followed by some keys."
        # NB. f1 works in ansi-term mode; C-h doesn't.
        actions.key("f1")
        if key is not None:
            actions.key(key)


@ctx.action_class("user")
class UserActions:
    def cut_line():
        actions.edit.line_start()
        actions.user.emacs("kill-line", 1)

    def split_window():
        actions.user.emacs("split-window-below")

    def split_window_vertically():
        actions.user.emacs("split-window-below")

    def split_window_up():
        actions.user.emacs("split-window-below")

    def split_window_down():
        actions.user.emacs("split-window-below")
        actions.user.emacs("other-window")

    def split_window_horizontally():
        actions.user.emacs("split-window-right")

    def split_window_left():
        actions.user.emacs("split-window-right")

    def split_window_right():
        actions.user.emacs("split-window-right")
        actions.user.emacs("other-window")

    def split_clear():
        actions.user.emacs("delete-window")

    def split_clear_all():
        actions.user.emacs("delete-other-windows")

    def split_reset():
        actions.user.emacs("balance-windows")

    def split_next():
        actions.user.emacs("other-window")

    def split_last():
        actions.user.emacs("other-window", -1)

    def split_flip():
        # only works reliably if there are only two panes/windows.
        actions.key("ctrl-x b enter ctrl-x o ctrl-x b enter")
        actions.user.split_last()
        actions.key("ctrl-x b enter ctrl-x o")

    def select_range(line_start, line_end):
        # Assumes transient mark mode.
        actions.edit.jump_line(line_start)
        actions.edit.jump_line(line_end + 1)
        actions.user.emacs("exchange-point-and-mark")

    # # Version that highlights without transient-mark-mode:
    # def select_range(line_start, line_end):
    #     actions.edit.jump_line(line_end + 1)
    #     actions.key("ctrl-@ ctrl-@")
    #     actions.edit.jump_line(line_start)

    # dictation_peek() probably won't work in a terminal. PRs welcome.
    def dictation_peek(left, right):
        # clobber transient selection if it exists
        actions.key("space backspace")
        before, after = None, None
        if left:
            actions.edit.extend_word_left()
            before = actions.edit.selected_text()
            actions.user.emacs("pop-to-mark-command")
        if right:
            actions.edit.extend_line_end()
            after = actions.edit.selected_text()
            actions.user.emacs("pop-to-mark-command")
        return (before, after)


@ctx.action_class("edit")
class EditActions:
    def save():
        actions.user.emacs("save-buffer")

    def save_all():
        actions.user.emacs("save-some-buffers")

    def copy():
        actions.user.emacs("kill-ring-save")

    def cut():
        actions.user.emacs("kill-region")

    def undo():
        actions.user.emacs("undo")

    def paste():
        actions.user.emacs("yank")

    def delete():
        actions.user.emacs("kill-region")

    def file_start():
        actions.user.emacs("beginning-of-buffer")

    def file_end():
        actions.user.emacs("end-of-buffer")

    # works for eg 'select to top', but not if preceded by other selections :(
    def extend_file_start():
        actions.user.emacs("beginning-of-buffer")

    def extend_file_end():
        actions.user.emacs("end-of-buffer")

    def select_none():
        actions.user.emacs("keyboard-quit")

    def select_all():
        actions.user.emacs("mark-whole-buffer")
        # If you don't use transient-mark-mode, maybe do this:
        # actions.key('ctrl-u ctrl-x ctrl-x')

    def word_left():
        actions.user.emacs("backward-word")

    def word_right():
        actions.user.emacs("forward-word")

    def extend_word_left():
        actions.user.emacs_meta("shift-b")

    def extend_word_right():
        actions.user.emacs_meta("shift-f")

    def sentence_start():
        actions.user.emacs("backward-sentence")

    def sentence_end():
        actions.user.emacs("forward-sentence")

    def extend_sentence_start():
        actions.user.emacs_meta("shift-a")

    def extend_sentence_end():
        actions.user.emacs_meta("shift-e")

    def paragraph_start():
        actions.user.emacs("backward-paragraph")

    def paragraph_end():
        actions.user.emacs("forward-paragraph")

    def line_start():
        actions.user.emacs("move-beginning-of-line")

    def line_end():
        actions.user.emacs("move-end-of-line")

    def extend_line_start():
        actions.key("shift-ctrl-a")

    def extend_line_end():
        actions.key("shift-ctrl-e")

    def line_swap_down():
        actions.key("down ctrl-x ctrl-t up")

    def line_swap_up():
        actions.key("ctrl-x ctrl-t up:2")

    def delete_line():
        actions.key("ctrl-a ctrl-k")

    def line_clone():
        actions.user.emacs_key("ctrl-a meta-1 ctrl-k ctrl-y ctrl-y up meta-m")

    def jump_line(n):
        actions.user.emacs("goto-line", n)

    def select_line(n: int = None):
        if n is not None:
            actions.edit.jump_line(n)
        else:
            actions.edit.line_start()
        actions.edit.extend_line_end()
        actions.edit.extend_right()
        # This makes it so the cursor is on the same line, which can make
        # subsequent commands more convenient.
        actions.user.emacs("exchange-point-and-mark")

    def indent_more():
        actions.user.emacs("indent-rigidly", 4)

    def indent_less():
        actions.user.emacs("indent-rigidly", -4)

    # These all perform text-scale-adjust, which examines the actual key pressed, so can't
    # be done with actions.user.emacs.
    def zoom_in():
        actions.key("ctrl-x ctrl-+")

    def zoom_out():
        actions.key("ctrl-x ctrl--")

    def zoom_reset():
        actions.key("ctrl-x ctrl-0")

    # Some modes override ctrl-s/r to do something other than isearch-forward, so we
    # deliberately don't use actions.user.emacs.
    def find(text: str = None):
        actions.key("ctrl-s")
        if text:
            actions.insert(text)

    def find_next():
        actions.key("ctrl-s")

    def find_previous():
        actions.key("ctrl-r")


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.user.emacs("make-frame-command")

    def tab_next():
        actions.user.emacs("tab-next")

    def tab_previous():
        actions.user.emacs("tab-previous")

    def tab_close():
        actions.user.emacs("tab-close")

    def tab_reopen():
        actions.user.emacs("tab-undo")

    def tab_open():
        actions.user.emacs("tab-new")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.user.emacs("comment-dwim")

    def language():
        # Assumes win.filename() gives buffer name.
        if "*scratch*" == actions.win.filename():
            return "elisp"
        return actions.next()


@ctx.action_class("win")
class WinActions:
    # This assumes the title is/contains the filename.
    # To do this, put this in init.el:
    # (setq-default frame-title-format '((:eval (buffer-name (window-buffer (minibuffer-selected-window))))))
    def filename():
        return actions.win.title()
