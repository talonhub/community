from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.git_hub_desktop = """
os: mac
and app.bundle: com.github.GitHubClient
"""