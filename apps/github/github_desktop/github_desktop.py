from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.apps.git_hub_desktop = """
os: mac
and app.bundle: com.github.GitHubClient
"""
mod.apps.git_hub_desktop = r"""
os: windows
and app.name: GitHubDesktop.exe
os: windows
and app.exe: /^githubdesktop\.exe$/i
"""