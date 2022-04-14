from talon import Context, actions, Module

# App definition
mod = Module()
mod.apps.terminator = """
os: linux
and app.exe: terminator
os: linux
and app.name: Terminator
"""

# Context matching
ctx = Context()
ctx.matches = r"""
app: terminator
"""
ctx.tags = [
    'terminal',
    'user.tabs',
    'user.splits',
    'user.generic_unix_shell',
    'user.git',
    'user.kubectl',
]


# --- Implement actions ---
@ctx.action_class('user')
class user_actions:
    # user.splits
    def split_window_right(): actions.key('alt-right')
    def split_window_left(): actions.key('alt-left')
    def split_window_down(): actions.key('alt-down')
    def split_window_up(): actions.key('alt-up')
    def split_window_vertically(): actions.key('shift-ctrl-e')
    def split_window_horizontally(): actions.key('shift-ctrl-o')
    def split_flip(): actions.key('super-r')
    def split_maximize(): actions.key('shift-ctrl-x')
    def split_reset(): actions.key('shift-ctrl-x')
    def split_window(): actions.key('shift-ctrl-o')
    def split_clear(): actions.key('shift-ctrl-r')
    def split_clear_all(): actions.key('shift-ctrl-g')
    def split_next(): actions.key('shift-ctrl-n')
    def split_last(): actions.key('shift-ctrl-p')


@ctx.action_class('app')
class AppActions:

    # app.tabs
    def tab_open(): actions.key('ctrl-shift-t')
    def tab_previous(): actions.key('ctrl-pageup')
    def tab_next(): actions.key('ctrl-pagedown')
    def tab_close(): actions.key('ctrl-shift-w')
    # global (overwrite linux/app.py)
    def window_open(): actions.key('ctrl-shift-i')
    def window_close(): actions.key('ctrl-shift-q')


# global (overwrite linux/edit.py)
@ctx.action_class('edit')
class EditActions:
    def page_down(): actions.key('shift-pagedown')
    def page_up(): actions.key('shift-pageup')
    def paste(): actions.key('ctrl-shift-v')
    def copy(): actions.key('ctrl-shift-c')

    def find(text: str = None):
        actions.key('ctrl-shift-f')
        if text:
            actions.insert(text)

    def delete_line():
        actions.edit.line_start()
        actions.key('ctrl-k')
