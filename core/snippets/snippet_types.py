from dataclasses import dataclass

from talon import Context


class SnippetLists:
    insertion: dict[str, str]
    with_phrase: dict[str, str]
    wrapper: dict[str, str]

    def __init__(self):
        self.insertion = {}
        self.with_phrase = {}
        self.wrapper = {}


@dataclass
class SnippetLanguageState:
    ctx: Context
    lists: SnippetLists


@dataclass
class SnippetVariable:
    name: str
    insertion_formatters: list[str] | None = None
    wrapper_phrases: list[str] | None = None
    wrapper_scope: str | None = None


@dataclass
class Snippet:
    name: str
    body: str
    description: str | None
    phrases: list[str] | None
    insertion_scopes: list[str] | None
    languages: list[str] | None
    variables: list[SnippetVariable]

    def get_variable(self, name: str):
        for var in self.variables:
            if var.name == name:
                return var
        return None

    def get_variable_strict(self, name: str):
        variable = self.get_variable(name)
        if variable is None:
            raise ValueError(f"Snippet '{self.name}' has no variable '{name}'")
        return variable


@dataclass
class InsertionSnippet:
    body: str
    scopes: list[str] | None
    languages: list[str] | None


@dataclass
class WrapperSnippet:
    body: str
    variable_name: str
    scope: str | None
    languages: list[str] | None
