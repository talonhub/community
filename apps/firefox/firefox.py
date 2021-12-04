from talon import ctrl, ui, Module, Context, actions, clip, app

ctx = Context()
mod = Module()
apps = mod.apps
apps.firefox = "app.name: Firefox"
apps.firefox = "app.name: Firefox Developer Edition"
apps.firefox = "app.name: firefox"
apps.firefox = """
os: windows
and app.name: Firefox
os: windows
and app.exe: firefox.exe
"""
apps.firefox = """
os: mac
and app.bundle: org.mozilla.firefox
"""

ctx.matches = r"""
app: firefox
"""

@ctx.action_class('browser')
class BrowserActions:
    # TODO
    #action(browser.address):
    #action(browser.title):
    def go(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        actions.key("enter")    
    def focus_search():
        actions.browser.focus_address()
    def submit_form():
        actions.key('enter')

