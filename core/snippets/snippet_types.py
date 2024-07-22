from dataclasses import dataclass


@dataclass
class SnippetVariable:
    name: str
    insertion_formatters: list[str] = None
    wrapper_phrases: list[str] = None
    wrapper_scope: str = None


@dataclass
class Snippet:
    name: str
    body: str
    phrases: list[str] = None
    insertion_scopes: list[str] = None
    languages: list[str] = None
    variables: list[SnippetVariable] = None

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
    scopes: list[str] = None


@dataclass
class WrapperSnippet:
    body: str
    variable_name: str
    scope: str = None
