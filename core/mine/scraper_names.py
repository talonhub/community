"""
This module gives us the list {} and the capture <user.system_path> that wraps
the list to easily refer to system paths in talon and python files. It also creates a file
system_paths.csv in the settings folder so they user can easily add their own custom paths.
"""
import os

from talon import Context, Module, actions, app

mod = Module()
ctx = Context()

mod.list("scraper_names", desc="List of system paths")


# We need to wait for ready before we can call "actions.path.talon_home()" and
# "actions.path.talon_user()"
def on_ready():
    default_system_paths = {
        "doordash revisit": "doordash_revisit",
    }

    ctx.lists["user.scraper_names"] = default_system_paths


@mod.capture(rule="{user.scraper_names}")
def scraper_names(m) -> str:
    return m.scraper_names


app.register("ready", on_ready)
