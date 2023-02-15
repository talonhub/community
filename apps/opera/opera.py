from talon import Context, actions

ctx = Context()
apps = mod.apps
apps.opera = "app.name: Opera"
apps.opera = "app.name: Opera Internet Browser"
apps.opera = """
os: mac
and app.bundle: com.operasoftware.Opera
"""
apps.opera = """
os: windows
and app.exe: opera.exe
"""
apps.opera = """
  os: linux
and app.exe: opera
"""


ctx.matches = r"""
app: opera
"""


@ctx.action_class("user")
class UserActions:
    def tab_close_wrapper():
        actions.sleep("180ms")
        actions.app.tab_close()


@ctx.action_class("browser")
class BrowserActions:
    def reload_hard():
        actions.key("shift-f5")
