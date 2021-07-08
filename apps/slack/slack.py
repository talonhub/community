from talon import Module

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
