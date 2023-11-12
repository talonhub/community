import re
from typing import Any

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
                reg = re.compile(rf"\${k}|\$\{{{k}\}}")
                if not reg.search(body):
                    raise ValueError(
                        f"Can't substitute non existing variable '{k}' in snippet '{name}'"
                    )
                body = reg.sub(v, body)

        actions.user.insert_snippet(body)

    def insert_snippet_by_name_with_phrase(name: str, phrase: str):
        """Insert snippet <name> with phrase <phrase>"""
        snippet: Snippet = actions.user.get_snippet(name)
        substitutions = {}

        for variable in snippet.variables:
            if variable.insertion_formatters is not None:
                formatters = ",".join(variable.insertion_formatters)
                formatted_phrase = actions.user.formatted_text(phrase, formatters)
                substitutions[variable.name] = formatted_phrase

        if not substitutions:
            raise ValueError(
                f"Can't use snippet phrase. No variable with insertion formatter in snippet '{name}'"
            )

        actions.user.insert_snippet_by_name(name, substitutions)

    def insert_wrapper_snippet(
        body: str,
        target: Any,
        scope: str = None,
    ):
        """Wrap the target with snippet"""

    def insert_wrapper_snippet_by_name(name: str, target: Any):
        """Wrap the target with snippet <name>"""
        index = name.rindex(".")
        snippet_name = name[:index]
        variable_name = name[index + 1]
        snippet: Snippet = actions.user.get_snippet(snippet_name)
        variable = snippet.get_variable_strict(variable_name)
        reg = re.compile(rf"\${variable_name}|\$\{{{variable_name}\}}")

        if not reg.search(snippet.body):
            raise ValueError(
                f"Can't wrap non existing variable '{variable_name}' in snippet body '{snippet.body}'"
            )

        body = reg.sub("$TM_SELECTED_TEXT", snippet.body)

        actions.user.insert_wrapper_snippet(body, target, variable.wrapper_scope)
