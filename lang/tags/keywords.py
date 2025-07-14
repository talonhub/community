from talon import Module, actions

mod = Module()

mod.tag("code_keywords", desc="Tag for enabling commands for keywords")

mod.list("code_keyword", desc="List of keywords for active language")
mod.list(
    "code_keyword_bare",
    desc="List of keywords for active language that can be dictated with just their names or the put command",
)


@mod.capture(rule=("{user.code_keyword}|{user.code_keyword_bare}"))
def code_keyword(m) -> str:
    return str(m)


@mod.action_class
class Actions:
    def code_keyword(keywords: list[str]):
        """Adds keywords"""
        for keyword in keywords:
            actions.insert(keyword)
