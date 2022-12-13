from talon import Context, actions
ctx = Context()
ctx.matches = r"""
os: mac
app: firefox
"""

@ctx.action_class('browser')
class BrowserActions:
    def bookmark():
        actions.key('cmd-d')
    def bookmark_tabs():
        actions.key('cmd-shift-d')
    def bookmarks():
        actions.key('cmd-alt-b')
        #action(browser.bookmarks_bar):
        #	key(ctrl-shift-b)
    def focus_address():
        actions.key('cmd-l')
        #action(browser.focus_page):
    def go_blank():
        actions.key('cmd-n')
    def go_back():
        actions.key('cmd-left')
    def go_forward():
        actions.key('cmd-right')
    def go_home():
        actions.key('cmd-shift-h')
    def open_private_window():
        actions.key('cmd-shift-p')
    def reload():
        actions.key('cmd-r')
    def reload_hard():
        actions.key('cmd-shift-r')
        #action(browser.reload_hardest):
    def show_clear_cache():
        actions.key('cmd-shift-delete')
    def show_downloads():
        actions.key('cmd-shift-j')
    def show_extensions():
        actions.key('cmd-shift-a')
    def show_history():
        actions.key('cmd-y')
    def toggle_dev_tools():
        actions.key('cmd-alt-i')

@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            actions.key("cmd-{}".format(number))

    def tab_final():
        actions.key("cmd-9")
