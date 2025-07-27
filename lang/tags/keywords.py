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
            num_leading_spaces = compute_number_of_leading_spaces(keywords[0])
            num_trailing_spaces = compute_number_of_trailing_spaces(keywords[-1])
            stripped_words = [word.strip() for word in keywords]
            combined_text = (
                " " * num_leading_spaces
                + " ".join(stripped_words)
                + " " * num_trailing_spaces
            )
            actions.insert(combined_text)


def compute_number_of_leading_spaces(text: str) -> int:
    num_leading_spaces = 0
    while text[num_leading_spaces] == " " and len(text) > num_leading_spaces:
        num_leading_spaces += 1
    return num_leading_spaces


def compute_number_of_trailing_spaces(text: str) -> int:
    num_trailing_spaces = 0
    while text[-(num_trailing_spaces + 1)] == " " and len(text) > num_trailing_spaces:
        num_trailing_spaces += 1
    return num_trailing_spaces
