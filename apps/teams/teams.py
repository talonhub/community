from talon import Module

mod = Module()
apps = mod.apps
apps.microsoft_teams = """
os: linux
and app.name: /teams/
os: linux
and app.name: /Teams/
"""
mod.apps.microsoft_teams = """
os: windows
and app.name: Microsoft Teams
os: windows
and app.exe: Teams.exe
"""
mod.apps.microsoft_teams = """
os: windows
and app.name: Microsoft Teams (work or school)
os: windows
and app.exe: ms-teams.exe
"""
mod.apps.microsoft_teams_work_or_school = r"""
os: windows
and app.name: Microsoft Teams (work or school)
os: windows
and app.exe: /^ms\-teams\.exe$/i
"""

mod.list("teams_alias", desc="list of teams user aliases")
