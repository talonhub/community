from pathlib import Path
from typing import Union

from talon import Context, Module, actions, app, fs, settings

from ..modes.code_languages import code_languages
from .snippet_types import (
    InsertionSnippet,
    Snippet,
    SnippetLanguageState,
    SnippetLists,
    WrapperSnippet,
)
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

# `_` represents the global context, ie snippets available regardless of language
GLOBAL_ID = "_"

# { SNIPPET_NAME: Snippet[] }
snippets_map: dict[str, list[Snippet]] = {}

# { LANGUAGE_ID: SnippetLanguageState }
languages_state_map: dict[str, SnippetLanguageState] = {
    GLOBAL_ID: SnippetLanguageState(Context(), SnippetLists())
}

# Create a context for each defined language
for lang in code_languages:
    ctx = Context()
    ctx.matches = f"code.language: {lang.id}"
    languages_state_map[lang.id] = SnippetLanguageState(ctx, SnippetLists())


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
    def get_snippets(name: str) -> list[Snippet]:
        """Get snippets named <name>"""
        if name not in snippets_map:
            raise ValueError(f"Unknown snippet '{name}'")
        return snippets_map[name]

    def get_snippet(name: str) -> Snippet:
        """Get snippet named <name> for the active language"""
        snippets: list[Snippet] = actions.user.get_snippets(name)
        return get_preferred_snippet(snippets)

    def get_insertion_snippets(name: str) -> list[InsertionSnippet]:
        """Get insertion snippets named <name>"""
        snippets: list[Snippet] = actions.user.get_snippets(name)
        return [
            InsertionSnippet(s.body, s.insertion_scopes, s.languages) for s in snippets
        ]

    def get_insertion_snippet(name: str) -> InsertionSnippet:
        """Get insertion snippet named <name> for the active language"""
        snippet: Snippet = actions.user.get_snippet(name)
        return InsertionSnippet(
            snippet.body,
            snippet.insertion_scopes,
            snippet.languages,
        )

    def get_wrapper_snippets(name: str) -> list[WrapperSnippet]:
        """Get wrapper snippets named <name>"""
        snippet_name, variable_name = split_wrapper_snippet_name(name)
        snippets: list[Snippet] = actions.user.get_snippets(snippet_name)
        return [to_wrapper_snippet(s, variable_name) for s in snippets]

    def get_wrapper_snippet(name: str) -> WrapperSnippet:
        """Get wrapper snippet named <name> for the active language"""
        snippet_name, variable_name = split_wrapper_snippet_name(name)
        snippet: Snippet = actions.user.get_snippet(snippet_name)
        return to_wrapper_snippet(snippet, variable_name)


def get_preferred_snippet(snippets: list[Snippet]) -> Snippet:
    lang: Union[str, set[str]] = actions.code.language()
    languages = [lang] if isinstance(lang, str) else lang

    # First try to find a snippet matching the active language
    for snippet in snippets:
        if snippet.languages:
            for snippet_lang in snippet.languages:
                if snippet_lang in languages:
                    return snippet

    # Then look for a global snippet
    for snippet in snippets:
        if not snippet.languages:
            return snippet

    raise ValueError(f"Snippet not available for language '{lang}'")


def split_wrapper_snippet_name(name: str) -> tuple[str, str]:
    index = name.rindex(".")
    return name[:index], name[index + 1]


def to_wrapper_snippet(snippet: Snippet, variable_name) -> WrapperSnippet:
    """Get wrapper snippet named <name>"""
    var = snippet.get_variable_strict(variable_name)
    return WrapperSnippet(
        snippet.body,
        var.name,
        var.wrapper_scope,
        snippet.languages,
    )


def update_snippets():
    global snippets_map

    snippets = get_snippets_from_files()
    name_to_snippets: dict[str, list[Snippet]] = {}
    language_to_lists: dict[str, SnippetLists] = {}

    for snippet in snippets:
        # Map snippet names to actual snippets
        name_to_snippets.setdefault(snippet.name, []).append(snippet)

        # Map languages to phrase / name dicts
        for language in snippet.languages or [GLOBAL_ID]:
            lists = language_to_lists.setdefault(language, SnippetLists())

            for phrase in snippet.phrases or []:
                lists.insertion[phrase] = snippet.name

                for var in snippet.variables:
                    if var.insertion_formatters:
                        lists.with_phrase[phrase] = snippet.name

            for var in snippet.variables:
                for phrase in var.wrapper_phrases or []:
                    lists.wrapper[phrase] = f"{snippet.name}.{var.name}"

    snippets_map = name_to_snippets
    update_contexts(language_to_lists)


def update_contexts(language_to_lists: dict[str, SnippetLists]):
    global_lists = language_to_lists[GLOBAL_ID] or SnippetLists()

    for lang, lists in language_to_lists.items():
        if lang not in languages_state_map:
            print(f"Found snippets for unknown language: {lang}")
            actions.app.notify(f"Found snippets for unknown language: {lang}")
            continue

        state = languages_state_map[lang]
        insertion = {**global_lists.insertion, **lists.insertion}
        with_phrase = {**global_lists.with_phrase, **lists.with_phrase}
        wrapper = {**global_lists.wrapper, **lists.wrapper}
        updated_lists: dict[str, dict[str, str]] = {}

        if state.lists.insertion != insertion:
            state.lists.insertion = insertion
            updated_lists["user.snippet"] = insertion

        if state.lists.with_phrase != with_phrase:
            state.lists.with_phrase = with_phrase
            updated_lists["user.snippet_with_phrase"] = with_phrase

        if state.lists.wrapper != wrapper:
            state.lists.wrapper = wrapper
            updated_lists["user.snippet_wrapper"] = wrapper

        if updated_lists:
            state.ctx.lists.update(updated_lists)


def get_snippets_from_files() -> list[Snippet]:
    setting_dir = get_setting_dir()
    result = []

    for file in SNIPPETS_DIR.glob("**/*.snippet"):
        result.extend(create_snippets_from_file(file))

    if setting_dir:
        for file in setting_dir.glob("**/*.snippet"):
            result.extend(create_snippets_from_file(file))

    return result


def on_ready():
    fs.watch(SNIPPETS_DIR, lambda _path, _flags: update_snippets())

    if get_setting_dir():
        fs.watch(get_setting_dir(), lambda _path, _flags: update_snippets())

    update_snippets()


app.register("ready", on_ready)
