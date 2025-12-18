from talon import Context, Module

from ..user_settings import track_csv_list

mod = Module()
mod.list("top_level_domain", desc="A top level domain, such as .com")

_top_level_domains_defaults = {
	"dot com": ".com",
	"dot net": ".net",
	"dot org": ".org",
    "dot education": ".edu",
    "dot e d u": ".edu",
	"dot us": ".us",
    "dot U S": ".us",
	"dot co dot UK": ".co.uk",
}

ctx = Context()

@track_csv_list(
    "top_level_domains.csv",
    headers=("File extension", "Name"),
    default=_top_level_domains_defaults,
)
def on_update(values):
    ctx.lists["self.top_level_domain"] = values
