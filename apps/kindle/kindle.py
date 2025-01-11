from talon import Context, actions, Module

# --- App definition ---
mod = Module()
mod.apps.kindle = r"""
os: windows
and app.name: Kindle
os: windows
and app.exe: /^kindle\.exe$/i
"""
mod.apps.kindle = """
os: mac
and app.bundle: com.amazon.Lassen
"""

ctx_win = Context()
ctx_win.matches = """
os: windows
app: kindle
"""

ctx_mac = Context()
ctx_mac.matches = """
os: mac
app: kindle
"""

@ctx_win.action_class("user")
class UserActions:
    # user.pages
    def page_next():
        actions.key("down")

    def page_previous():
        actions.key("up")

    def page_jump(number: int):
        actions.key("ctrl-g")
        actions.insert(str(number))
        actions.key("enter")
@ctx_mac.action_class("user")
class UserActions:
    # user.pages
    def page_next():
        actions.key("down")

    def page_previous():
        actions.key("up")

    # def page_jump(number: int):
    #     actions.key("ctrl-g")
    #     actions.insert(str(number))
    #     actions.key("enter")