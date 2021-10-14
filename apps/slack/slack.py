from talon import Context, Module, actions

ctx = Context()
mod = Module()
apps = mod.apps
apps.slack = "app.name: Slack"
mod.apps.slack = """
os: windows
and app.name: Slack
os: windows
and app.exe: slack.exe
"""
apps.slack = """
os: mac
and app.bundle: com.tinyspeck.slackmacgap
"""
ctx.matches = r"""
app: slack
"""

@ctx.action_class("edit")
class EditActions:
    def line_insert_down():
        actions.edit.line_end()
        actions.key("shift-enter")
