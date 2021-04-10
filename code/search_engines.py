from .user_settings import get_list_from_csv
from talon import Module, Context
from urllib.parse import quote_plus
import webbrowser

mod = Module()
mod.list(
    "search_engine",
    desc="A search engine.  Any instance of %s will be replaced by query text",
)


ctx = Context()
ctx.lists["self.search_engine"] = get_list_from_csv(
    "search_engines.csv", headers=("URL Template", "Name"),
)


@mod.action_class
class Actions:
    def search_with_search_engine(search_template: str, search_text: str):
        """Search a search engine for given text"""
        url = search_template.replace("%s", quote_plus(search_text))
        webbrowser.open(url)
