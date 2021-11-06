from talon import ctrl, ui, Module, Context, actions, clip, app
from talon.mac import applescript

ctx = Context()
mod = Module()

mod.apps.chrome = "app.name: Google Chrome"
mod.apps.chrome = """
os: windows
and app.name: Google Chrome
os: windows
and app.exe: chrome.exe
"""
mod.apps.chrome = """
os: mac
and app.bundle: com.google.Chrome
"""
ctx.matches = r"""
app: chrome
"""


@ctx.action_class("user")
class user_actions:
    def tab_jump(number: int):
        if number < 9:
            if app.platform == "mac":
                actions.key("cmd-{}".format(number))
            else:
                actions.key("ctrl-{}".format(number))

    def tab_final():
        if app.platform == "mac":
            actions.key("cmd-9")
        else:
            actions.key("ctrl-9")

    def tab_close_wrapper():
        actions.sleep("180ms")
        actions.app.tab_close()

def chrome_app():
    return ui.apps(bundle="com.google.Chrome")[0]

@ctx.action_class("browser")
class browser_actions:
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
    def go(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        actions.key("enter")
