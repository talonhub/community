from dataclasses import dataclass


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
    phrases: list[str] | None = None
    insertion_scopes: list[str] | None = None
    languages: list[str] | None = None
    variables: list[SnippetVariable] | None = None

    def get_variable(self, name: str):
        if self.variables:
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
    scopes: list[str] | None = None


@dataclass
class WrapperSnippet:
    body: str
    variable_name: str
    scope: str | None = None
