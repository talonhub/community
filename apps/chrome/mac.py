from talon import Context, actions, ui
from talon.mac import applescript

ctx = Context()
ctx.matches = r"""
os: mac
app: chrome
"""
ctx.tags = ['browser', 'user.tabs']

def chrome_app():
    return ui.apps(bundle="com.google.Chrome")[0]

@ctx.action_class('browser')
class BrowserActions:
    def address() -> str:
        try:
            window = chrome_app().windows()[0]
        except IndexError:
            return ''
        try:
            web_area = window.element.children.find_one(AXRole='AXWebArea')
            address = web_area.AXURL
        except (ui.UIErr, AttributeError):
            address = applescript.run('''
                tell application id "com.google.Chrome"
                    if not (exists (window 1)) then return ""
                    return window 1's active tab's URL
                end tell
            ''')
        return address
    def bookmark():
        actions.key('cmd-d')
    def bookmark_tabs():
        actions.key('cmd-shift-d')
    def bookmarks():
        actions.key('cmd-alt-b')
    def bookmarks_bar():
        actions.key('cmd-shift-b')
    def focus_address():
        actions.key('cmd-l')
        #action(browser.focus_page):
    def focus_search():
        actions.browser.focus_address()
    def go_blank():
        actions.key('cmd-n')
    def go_back():
        actions.key('cmd-[')
    def go_forward():
        actions.key('cmd-]')
    def go_home():
        actions.key('cmd-shift-h')
    def open_private_window():
        actions.key('cmd-shift-n')
    def reload():
        actions.key('cmd-r')
    def reload_hard():
        actions.key('cmd-shift-r')
        #action(browser.reload_hardest):
    def show_clear_cache():
        actions.key('cmd-shift-delete')
    def show_downloads():
        actions.key('cmd-shift-j')
        #action(browser.show_extensions)
    def show_history():
        actions.key('cmd-y')
    def submit_form():
        actions.key('enter')
        #action(browser.title)
    def toggle_dev_tools():
        actions.key('cmd-alt-i')
