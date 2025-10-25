import re

from talon import Module, actions, settings

from .snippet_types import Snippet
from .snippets_insert_raw_text import go_to_next_stop_raw, insert_snippet_raw_text
from .snippets_parser import add_final_stop_to_snippet_body

mod = Module()


@mod.action_class
class Actions:
    def insert_snippet(body: str):
        """Insert snippet"""
        insert_snippet_raw_text(body)

    def move_cursor_to_next_snippet_stop():
        """Moves the cursor to the next snippet stop"""
        go_to_next_stop_raw()

    def insert_snippet_by_name(
        name: str,
        substitutions: dict[str, str] = None,
    ):
        """Insert snippet <name>"""
        body = get_snippet_body_by_name_with_substitutions(name, substitutions)
        actions.user.insert_snippet(body)

    def insert_snippet_by_name_with_stop_at_end(
        name: str,
        substitutions: dict[str, str] = None,
    ):
        """Insert snippet <name> with a final stop guaranteed to be at the end of the snippet"""
        body = get_snippet_body_by_name_with_substitutions(name, substitutions)
        insert_snippet_with_stop_at_the_end(body)

    def insert_snippet_by_name_with_phrase(name: str, phrase: str):
        """Insert snippet <name> with phrase <phrase>"""
        body = get_snippet_body_by_name_with_phrase_substitutions(name, phrase)
        actions.user.insert_snippet(body)

    def insert_snippet_by_name_with_phrase_and_stop_at_end(name: str, phrase: str):
        """Insert snippet <name> with phrase <phrase> and a stop at the end"""
        body = get_snippet_body_by_name_with_phrase_substitutions(name, phrase)
        insert_snippet_with_stop_at_the_end(body)


def get_snippet_body_by_name_with_phrase_substitutions(name: str, phrase: str):
    snippet: Snippet = actions.user.get_snippet(name)
    substitutions = compute_phrase_substitutions(snippet, phrase)
    body = compute_snippet_body_with_substitutions(snippet, substitutions)
    return body


def get_snippet_body_by_name_with_substitutions(
    name: str, substitutions: dict[str, str]
) -> str:
    snippet: Snippet = actions.user.get_snippet(name)
    body = compute_snippet_body_with_substitutions(snippet, substitutions)
    return body


def insert_snippet_with_stop_at_the_end(body):
    body = add_final_stop_to_snippet_body(body)
    actions.user.insert_snippet(body)


def compute_snippet_body_with_substitutions(
    snippet: Snippet, substitutions: dict[str, str]
) -> str:
    body = snippet.body
    if substitutions:
        for k, v in substitutions.items():
            v = v.replace("$", r"\$")
            reg = re.compile(rf"\${k}|\$\{{{k}\}}")
            if not reg.search(body):
                raise ValueError(
                    f"Can't substitute non existing variable '{k}' in snippet '{snippet.name}'"
                )
            body = reg.sub(v, body)
    return body


def compute_phrase_substitutions(snippet: Snippet, phrase: str):
    substitutions = {}

    def get_setting(m: re.Match[str]):
        try:
            return str(settings.get(m.group(1)))
        except KeyError as ex:
            raise ValueError(
                f"Undefined formatter setting {ex} in snippet '{snippet.name}'"
            )

    for variable in snippet.variables:
        if variable.insertion_formatters is not None:
            formatters = ",".join(variable.insertion_formatters)
            formatters = re.sub(r"setting\(([\w.]+)\)", get_setting, formatters)
            formatted_phrase = actions.user.formatted_text(phrase, formatters)
            substitutions[variable.name] = formatted_phrase

    if not substitutions:
        raise ValueError(
            f"Can't use snippet phrase. No variable with insertion formatter in snippet '{snippet.name}'"
        )

    return substitutions
