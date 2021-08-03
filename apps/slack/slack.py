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

@ctx.action_class("user")
class UserActions:
    def create_blank_line():
        actions.edit.line_end()
        actions.key("shift-enter")