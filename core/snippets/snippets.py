import glob
from collections import defaultdict
from pathlib import Path

from talon import Context, Module, actions, app, fs, settings

from ..modes.language_modes import language_ids
from .snippet_types import InsertionSnippet, Snippet, WrapperSnippet
from .snippets_parser import create_snippets_from_file

SNIPPETS_DIR = Path(__file__).parent / "snippets"

mod = Module()

mod.list("snippet", "List of insertion snippets")
mod.list("snippet_with_phrase", "List of insertion snippets containing a text phrase")
mod.list("snippet_wrapper", "List of wrapper snippets")

mod.setting(
    "snippets_dir",
    type=str,
    default=None,
    desc="Directory (relative to Talon user) containing additional snippets",
)

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


def get_setting_dir():
    setting_dir = settings.get("user.snippets_dir")
    if not setting_dir:
        return None

    dir = Path(setting_dir)

    if not dir.is_absolute():
        user_dir = Path(actions.path.talon_user())
        dir = user_dir / dir

    return dir.resolve()


@mod.action_class
class Actions:
    def get_snippet(name: str) -> Snippet:
        """Get snippet named <name>"""
        # Add current code language if not specified
        if "." not in name:
            lang = actions.code.language() or "_"
            name = f"{lang}.{name}"

        if name not in snippets_map:
            raise ValueError(f"Unknown snippet '{name}'")

        return snippets_map[name]

    def get_insertion_snippet(name: str) -> InsertionSnippet:
        """Get insertion snippet named <name>"""
        snippet: Snippet = actions.user.get_snippet(name)
        return InsertionSnippet(snippet.body, snippet.insertion_scopes)

    def get_wrapper_snippet(name: str) -> WrapperSnippet:
        """Get wrapper snippet named <name>"""
        index = name.rindex(".")
        snippet_name = name[:index]
        variable_name = name[index + 1]
        snippet: Snippet = actions.user.get_snippet(snippet_name)
        variable = snippet.get_variable_strict(variable_name)
        return WrapperSnippet(snippet.body, variable.name, variable.wrapper_scope)


def update_snippets():
    language_to_snippets = group_by_language(get_snippets())

    snippets_map.clear()

    for lang, ctx in context_map.items():
        insertion_map = {}
        insertions_phrase_map = {}
        wrapper_map = {}

        for lang_super in get_super_languages(lang):
            snippets, insertions, insertions_phrase, wrappers = create_lists(
                lang,
                lang_super,
                language_to_snippets.get(lang_super, []),
            )
            snippets_map.update(snippets)
            insertion_map.update(insertions)
            insertions_phrase_map.update(insertions_phrase)
            wrapper_map.update(wrappers)

        ctx.lists.update(
            {
                "user.snippet": insertion_map,
                "user.snippet_with_phrase": insertions_phrase_map,
                "user.snippet_wrapper": wrapper_map,
            }
        )


def get_snippets() -> list[Snippet]:
    files = glob.glob(f"{SNIPPETS_DIR}/**/*.snippet", recursive=True)

    if get_setting_dir():
        files.extend(glob.glob(f"{get_setting_dir()}/**/*.snippet", recursive=True))

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
    lang_ctx: str,
    lang_snippets: str,
    snippets: list[Snippet],
) -> tuple[dict[str, list[Snippet]], dict[str, str], dict[str, str], dict[str, str]]:
    """Creates the lists for the given language, and returns them as a tuple of (snippets, insertions, insertions_phrase, wrappers)

    Args:
        lang_ctx (str): The language of the context match
        lang_snippets (str): The language of the snippets
        snippets (list[Snippet]): The list of snippets for the given language
    """
    snippets_map = {}
    insertions = {}
    insertions_phrase = {}
    wrappers = {}

    for snippet in snippets:
        id_ctx = f"{lang_ctx}.{snippet.name}"
        id_lang = f"{lang_snippets}.{snippet.name}"

        # Make sure that the snippet is added to the map for the context language
        snippets_map[id_ctx] = snippet

        if snippet.phrases is not None:
            for phrase in snippet.phrases:
                insertions[phrase] = id_lang

        if snippet.variables is not None:
            for var in snippet.variables:
                if var.insertion_formatters is not None and snippet.phrases is not None:
                    for phrase in snippet.phrases:
                        insertions_phrase[phrase] = id_lang

                if var.wrapper_phrases is not None:
                    for phrase in var.wrapper_phrases:
                        wrappers[phrase] = f"{id_lang}.{var.name}"

    return snippets_map, insertions, insertions_phrase, wrappers


def on_ready():
    fs.watch(str(SNIPPETS_DIR), lambda _1, _2: update_snippets())

    if get_setting_dir():
        fs.watch(str(get_setting_dir()), lambda _1, _2: update_snippets())

    update_snippets()


app.register("ready", on_ready)
