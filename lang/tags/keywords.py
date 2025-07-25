from talon import Module, actions

mod = Module()

mod.tag("code_keywords", desc="Tag for enabling commands for keywords")

mod.list("code_keyword", desc="List of keywords for active language")
mod.list(
    "code_keyword_bare",
    desc="List of keywords for active language that can be dictated by name alone or the put (name) command",
)


@mod.capture(rule=("{user.code_keyword}|{user.code_keyword_bare}"))
def code_keyword(m) -> str:
    return str(m)


@mod.action_class
class Actions:
    def code_keyword(keywords: list[str]):
        """Adds keywords"""
        if len(keywords) == 1:
            actions.insert(keywords[0])
        else:
            # every keyword is separated by a space
            # the spacing before the first keyword and after the last keyword is kept
            combined_text: str = keywords[0].rstrip() + " "
            for i in range(1, len(keywords) - 1):
                combined_text += keywords[i].strip() + " "
            combined_text += keywords[-1].lstrip()
            actions.insert(combined_text)
