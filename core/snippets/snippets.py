from collections import defaultdict
import glob
from pathlib import Path

from talon import Context, Module, app, fs

from ..modes.language_modes import language_ids
from .snippet_types import Snippet
from .snippets_parser import create_snippets_from_file

SNIPPETS_DIR = Path(__file__).parent / "snippets"

mod = Module()

mod.list("snippet_insert", "List of insertion snippets")
mod.list(
    "snippet_insert_with_phrase", "List of insertion snippets containing a text phrase"
)
mod.list("snippet_wrap", "List of wrapper snippets")

context_map = {
    # `_` represents the global context, ie snippets available regardless of language
    "_": Context(),
}
snippets_map = {}

# Create a context for each defined language
for lang in language_ids:
    ctx = Context()
    ctx.matches = f"code.language: {lang}"
    context_map[lang] = ctx


@mod.action_class
class Actions:
    def get_snippet(name: str) -> Snippet:
        """Get snippet named <name>"""
        return snippets_map[name]


def update_snippets():
    grouped = group_by_language(get_snippets())

    snippets_map.clear()

    for lang, ctx in context_map.items():
        insertion_map = {}
        insertions_phrase_map = {}
        wrapper_map = {}

        for sl in get_super_languages(lang):
            snippets, insertions, insertions_phrase, wrappers = create_lists(
                lang, sl, grouped.get(sl, [])
            )
            snippets_map.update(snippets)
            insertion_map.update(insertions)
            insertions_phrase_map.update(insertions_phrase)
            wrapper_map.update(wrappers)

        ctx.lists["user.snippet_insert"] = insertion_map
        ctx.lists["user.snippet_insert_with_phrase"] = insertions_phrase_map
        ctx.lists["user.snippet_wrap"] = wrapper_map


def get_snippets() -> list[Snippet]:
    files = glob.glob(f"{SNIPPETS_DIR}/*.snippet")
    result = []

    for file in files:
        result.extend(create_snippets_from_file(file))

    return result


def get_super_languages(language: str) -> list[str]:
    """Returns a list of languages that are considered a superset of <language>, including <language> itself. Eg `javascript` will be included in the list when <language> is `typescript`.
    Note that the order of languages returned here is very important: more general must precede more specific, so that specific langs can properly override general languages.
    """
    match language:
        case "_":
            return ["_"]
        case "typescript":
            return ["_", "javascript", "typescript"]
        case "javascriptreact":
            return ["_", "html", "javascript", "javascriptreact"]
        case "typescriptreact":
            return [
                "_",
                "html",
                "javascript",
                "typescript",
                "javascriptreact",
                "typescriptreact",
            ]
        case _:
            return ["_", language]


def group_by_language(snippets: list[Snippet]) -> dict[str, list[Snippet]]:
    result = defaultdict(list)
    for snippet in snippets:
        if snippet.languages is not None:
            for lang in snippet.languages:
                result[lang].append(snippet)
        else:
            result["_"].append(snippet)
    return result


def create_lists(
    lang_snippets: str,
    lang_ctx: str,
    snippets: list[Snippet],
) -> tuple[dict[str, list[Snippet]], dict[str, str], dict[str, str]]:
    snippets_map = {}
    insertions = {}
    insertions_phrase = {}
    wrappers = {}
    prefix_snippets = "" if lang_snippets == "_" else f"{lang_snippets}."
    prefix_ctx = "" if lang_ctx == "_" else f"{lang_ctx}."

    for snippet in snippets:
        id_snippets = f"{prefix_snippets}{snippet.name}"
        id_ctx = f"{prefix_ctx}{snippet.name}"

        snippets_map[id_snippets] = snippet

        if snippet.phrases is not None:
            for phrase in snippet.phrases:
                insertions[phrase] = id_ctx

        if snippet.variables is not None:
            for var in snippet.variables:
                if var.insertion_formatters is not None and snippet.phrases is not None:
                    for phrase in snippet.phrases:
                        insertions_phrase[phrase] = id_ctx

                if var.wrapper_phrases is not None:
                    for phrase in var.wrapper_phrases:
                        wrappers[phrase] = f"{id_ctx}.{var.name}"

    return snippets_map, insertions, insertions_phrase, wrappers


def on_ready():
    fs.watch(str(SNIPPETS_DIR), lambda _1, _2: update_snippets())
    update_snippets()


app.register("ready", on_ready)
