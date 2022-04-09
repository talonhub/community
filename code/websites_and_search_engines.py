from .user_settings import get_list_from_csv
from talon import Module, Context
from urllib.parse import quote_plus
import webbrowser

mod = Module()
mod.list("website", desc="A website.")
mod.list(
    "search_engine",
    desc="A search engine.  Any instance of %s will be replaced by query text",
)

website_defaults = {
    "talon home page":"http://talonvoice.com",
    "talon slack":"http://talonvoice.slack.com/messages/help",
    "talon wiki":"https://talon.wiki/",
    "talon practice":"https://chaosparrot.github.io/talon_practice/",
    "talon repository search": "https://search.talonvoice.com/search/",
    "amazon": "https://www.amazon.com/",
    "dropbox": "https://dropbox.com/",
    "google": "https://www.google.com/",
    "google calendar": "https://calendar.google.com",
    "google maps": "https://maps.google.com/",
    "google scholar": "https://scholar.google.com/",
    "gmail": "https://mail.google.com/",
    "github": "https://github.com/",
    "gist": "https://gist.github.com/",
    "wikipedia": "https://en.wikipedia.org/",
    "youtube": "https://www.youtube.com/",
}

_search_engine_defaults = {
    "amazon": "https://www.amazon.com/s/?field-keywords=%s",
    "google": "https://www.google.com/search?q=%s",
    "map": "https://maps.google.com/maps?q=%s",
    "scholar": "https://scholar.google.com/scholar?q=%s",
    "wiki": "https://en.wikipedia.org/w/index.php?search=%s",
}

ctx = Context()
ctx.lists["self.website"] = get_list_from_csv(
    "websites.csv",
    headers=("URL", "Spoken name"),
    default=website_defaults,
)
ctx.lists["self.search_engine"] = get_list_from_csv(
    "search_engines.csv",
    headers=("URL Template", "Name"),
    default=_search_engine_defaults,
)


@mod.action_class
class Actions:
    def open_url(url: str):
        """Visit the given URL."""
        webbrowser.open(url)

    def search_with_search_engine(search_template: str, search_text: str):
        """Search a search engine for given text"""
        url = search_template.replace("%s", quote_plus(search_text))
        webbrowser.open(url)
