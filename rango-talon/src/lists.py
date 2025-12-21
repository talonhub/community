from talon import Module, Context

mod = Module()
ctx = Context()
ctx.matches = r"""
tag: browser
"""

mod.list("rango_hints_toggle_levels", desc="list of Rango hints toggle levels")
mod.list(
    "rango_page_location_property",
    desc="list of properties to be found in window.location",
)
mod.list("rango_page", desc="A Rango-related page")

toggle_levels = ["everywhere", "global", "tab", "host", "page", "now"]
ctx.lists["user.rango_hints_toggle_levels"] = {k: k for k in toggle_levels}
ctx.lists["user.rango_page_location_property"] = {
    "address": "href",
    "host name": "hostname",
    "host": "host",
    "origin": "origin",
    "path": "pathname",
    "port": "port",
    "protocol": "protocol",
}
ctx.lists["user.rango_page"] = {
    "sponsor": "https://github.com/sponsors/david-tejada",
    "read me": "https://rango.click",
    "issues": "https://github.com/david-tejada/rango/issues",
    "new issue": "https://github.com/david-tejada/rango/issues/new",
    "changelog": "https://github.com/david-tejada/rango/blob/main/CHANGELOG.md",
}
