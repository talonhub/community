from talon import Module, Context
from urllib.parse import quote_plus
import webbrowser

mod = Module()
mod.list(
    "search_engine",
    desc="A search engine.  Any instance of %s will be replaced by query text",
)

ctx = Context()
ctx.lists["self.search_engine"] = {
    "google": "https://www.google.com/search?sclient=psy-ab&hl=en&site=&source=hp&q=%s&btnG=Search&pbx=1&oq=&aq=&aqi=&aql=&gs_sm=&gs_upl=",
    "wiki": "http://en.wikipedia.org/w/index.php?title=Special%3ASearch&search=%s&button=",
    "amazon": "http://smile.amazon.co.uk/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=%s",
    "map": "http://maps.google.com/maps?f=q&source=s_q&hl=en&q=%s",
    "scholar": "http://scholar.google.com/scholar?hl=en&q=%s&btnG=&as_sdt=1%2C5&as_sdtp=",
}


@mod.action_class
class Actions:
    def search_with_search_engine(search_template: str, search_text: str):
        """Search a search engine for given text"""
        url = search_template.replace("%s", quote_plus(search_text))
        webbrowser.open(url)