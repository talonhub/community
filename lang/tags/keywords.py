from talon import Module, actions

mod = Module()

mod.tag("code_keywords", desc="Tag for enabling commands for keywords")

mod.list("code_keyword", desc="List of keywords for active language")
mod.list("code_keyword_long", desc="List of long keywords (at least 3 syllables) for active language")


@mod.capture(rule=("{user.code_keyword}|{user.code_keyword_long}"))
def code_keyword(m) -> str:
    return str(m)


@mod.capture(rule=("{user.code_keyword_long}"))
def code_keyword_long(m) -> str:
    return str(m)


@mod.action_class
class Actions:
    def code_keyword(keywords: list[str]):
        """Adds keywords"""
        for keyword in keywords:
            actions.insert(keyword)
