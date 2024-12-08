import webbrowser
from urllib.parse import quote_plus

from talon import Context, Module

mod = Module()
mod.list("website", desc="A website.")
mod.list(
    "search_engine",
    desc="A search engine.  Any instance of %s will be replaced by query text",
)

ctx_browser = Context()
ctx_browser.matches = r"""
tag: browser
"""


@mod.action_class
class Actions:
    def open_url(url: str):
        """Visit the given URL."""
        webbrowser.open(url)

    def search_with_search_engine(search_template: str, search_text: str):
        """Search a search engine for given text"""
        url = search_template.replace("%s", quote_plus(search_text))
        webbrowser.open(url)


@ctx_browser.capture("user.address", rule="{user.website}")
def address(m) -> str:
    return m.website
