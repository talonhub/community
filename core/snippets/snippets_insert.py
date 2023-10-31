from talon import Module, actions
from .snippet_types import Snippet
from .snippets_insert_raw_text import insert_snippet_raw_text

mod = Module()


@mod.action_class
class Actions:
    def insert_snippet(body: str):
        """Insert snippet"""
        insert_snippet_raw_text(body)

    def insert_snippet_by_name(name: str, substitutions: dict[str, str] = None):
        """Insert snippet <name>"""
        snippet: Snippet = actions.user.get_snippet(name)
        body = snippet.body

        if substitutions:
            for k, v in substitutions.items():
                body = body.replace(f"${k}", v)

        actions.user.insert_snippet(body)

    def insert_snippet_by_name_with_phrase(name: str, phrase: str):
        """Insert snippet <name> with phrase <phrase>"""
        snippet: Snippet = actions.user.get_snippet(name)
        substitutions = {}

        for variable in snippet.variables:
            if variable.insertionFormatters is not None:
                formatters = ",".join(variable.insertionFormatters)
                formatted_phrase = actions.user.format_text(phrase, formatters)
                substitutions[variable.name] = formatted_phrase

        actions.user.insert_snippet_by_name(name, substitutions)

    def code_insert_snippet_by_name(name: str, substitutions: dict[str, str] = None):
        """Insert snippet <name> for the current programming language"""
        lang = actions.code.language()
        actions.user.insert_snippet_by_name(f"{lang}.{name}", substitutions)
