from dataclasses import dataclass


@dataclass
class SnippetVariable:
    name: str
    insertionFormatters: list[str] = None
    wrapperPhrases: list[str] = None
    wrapperScope: str = None


@dataclass
class Snippet:
    name: str
    body: str
    phrases: list[str] = None
    insertionScopes: list[str] = None
    languages: list[str] = None
    variables: list[SnippetVariable] = None

    def get_variable(self, name: str):
        if self.variables:
            for var in self.variables:
                if var.name == name:
                    return var
        return None

    def assert_get_variable(self, name: str):
        variable = self.get_variable(name)
        if variable is None:
            raise ValueError(f"Snippet '{self.name}' has no variable '{name}'")
        return variable
