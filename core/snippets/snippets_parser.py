import re
from pathlib import Path
from typing import Callable, Union

from .snippet_types import Snippet, SnippetVariable


class SnippetDocument:
    file: str
    line_doc: int
    line_body: int
    variables: list[SnippetVariable] = []
    name: str | None = None
    description: str | None = None
    phrases: list[str] | None = None
    insertionScopes: list[str] | None = None
    languages: list[str] | None = None
    body: str | None = None

    def __init__(self, file: str, line_doc: int, line_body: int):
        self.file = file
        self.line_doc = line_doc
        self.line_body = line_body


def create_snippets_from_file(file_path: str) -> list[Snippet]:
    documents = parse_file(file_path)
    return create_snippets(documents)


def create_snippets(documents: list[SnippetDocument]) -> list[Snippet]:
    if len(documents) == 0:
        return []

    if documents[0].body is None:
        default_context = documents[0]
        documents = documents[1:]
    else:
        default_context = SnippetDocument("", -1, -1)

    snippets: list[Snippet] = []

    for doc in documents:
        snippet = create_snippet(doc, default_context)
        if snippet:
            snippets.append(snippet)

    return snippets


def create_snippet(
    document: SnippetDocument,
    default_context: SnippetDocument,
) -> Snippet | None:
    snippet = Snippet(
        name=document.name or default_context.name or "",
        description=document.description or default_context.description,
        languages=document.languages or default_context.languages,
        phrases=document.phrases or default_context.phrases,
        insertion_scopes=document.insertionScopes or default_context.insertionScopes,
        variables=combine_variables(default_context.variables, document.variables),
        body=normalize_snippet_body_tabs(document.body),
    )

    if not validate_snippet(document, snippet):
        return None

    return snippet


def validate_snippet(document: SnippetDocument, snippet: Snippet) -> bool:
    is_valid = True

    if not snippet.name:
        error(document.file, document.line_doc, "Missing snippet name")
        is_valid = False

    if snippet.variables is None:
        error(document.file, document.line_doc, "Missing snippet variables")
        return False

    for variable in snippet.variables:
        var_name = f"${variable.name}"
        if var_name not in snippet.body:
            error(
                document.file,
                document.line_body,
                f"Variable '{var_name}' missing in body '{snippet.body}'",
            )
            is_valid = False

        if variable.insertion_formatters is not None and snippet.phrases is None:
            error(
                document.file,
                document.line_doc,
                f"Snippet phrase required when using '{var_name}.insertionFormatter'",
            )
            is_valid = False

        if variable.wrapper_scope is not None and variable.wrapper_phrases is None:
            error(
                document.file,
                document.line_doc,
                f"'{var_name}.wrapperPhrase' required when using '{var_name}.wrapperScope'",
            )
            is_valid = False

    return is_valid


def combine_variables(
    default_variables: list[SnippetVariable],
    document_variables: list[SnippetVariable],
) -> list[SnippetVariable]:
    variables: dict[str, SnippetVariable] = {}

    for variable in [*default_variables, *document_variables]:
        if variable.name not in variables:
            variables[variable.name] = SnippetVariable(variable.name)

        new_variable = variables[variable.name]

        if variable.insertion_formatters is not None:
            new_variable.insertion_formatters = variable.insertion_formatters

        if variable.wrapper_phrases is not None:
            new_variable.wrapper_phrases = variable.wrapper_phrases

        if variable.wrapper_scope is not None:
            new_variable.wrapper_scope = variable.wrapper_scope

    return list(variables.values())


def normalize_snippet_body_tabs(body: str | None) -> str:
    if not body:
        return ""

    # If snippet body already contains tabs. No change.
    if "\t" in body:
        return body

    lines = []
    smallest_indentation = None

    for line in body.splitlines():
        match = re.search(r"^\s+", line)
        indentation = match.group() if match is not None else ""

        # Keep track of smallest non-empty indentation
        if len(indentation) > 0 and (
            smallest_indentation is None or len(indentation) < len(smallest_indentation)
        ):
            smallest_indentation = indentation

        lines.append({"indentation": indentation, "rest": line[len(indentation) :]})

    # No indentation found in snippet body. No change.
    if smallest_indentation is None:
        return body

    normalized_lines = [
        reconstruct_line(smallest_indentation, line["indentation"], line["rest"])
        for line in lines
    ]

    return "\n".join(normalized_lines)


def reconstruct_line(smallest_indentation: str, indentation: str, rest: str) -> str:
    # Update indentation by replacing each occurrent of smallest space indentation with a tab
    indentation = indentation.replace(smallest_indentation, "\t")
    return f"{indentation}{rest}"


# ---------- Snippet file parser ----------


def parse_file(file_path: str) -> list[SnippetDocument]:
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    file_name = Path(file_path).name
    return parse_file_content(file_name, content)


def parse_file_content(file: str, text: str) -> list[SnippetDocument]:
    doc_texts = re.split(r"^---\n?$", text, flags=re.MULTILINE)
    documents: list[SnippetDocument] = []
    line = 0

    for i, doc_text in enumerate(doc_texts):
        optional_body = i == 0 and len(doc_texts) > 1
        document = parse_document(file, line, optional_body, doc_text)
        if document is not None:
            documents.append(document)
        line += doc_text.count("\n") + 1

    return documents


def parse_document(
    file: str,
    line: int,
    optional_body: bool,
    text: str,
) -> Union[SnippetDocument, None]:
    parts = re.split(r"^-$", text, maxsplit=1, flags=re.MULTILINE)
    line_body = line + parts[0].count("\n") + 1
    org_doc = SnippetDocument(file, line, line_body)
    document = parse_context(file, line, org_doc, parts[0])

    if len(parts) == 2:
        body = parse_body(parts[1])
        if body is not None:
            if document is None:
                document = org_doc
            document.body = body

    if document and not document.body and not optional_body:
        error(file, line, f"Missing body in snippet document '{text}'")
        return None

    return document


def parse_context(
    file: str,
    line: int,
    document: SnippetDocument,
    text: str,
) -> Union[SnippetDocument, None]:
    lines = [l.strip() for l in text.splitlines()]
    keys: set[str] = set()
    variables: dict[str, SnippetVariable] = {}

    def get_variable(name: str) -> SnippetVariable:
        if name not in variables:
            variables[name] = SnippetVariable(name)
        return variables[name]

    for i, line_text in enumerate(lines):
        if line_text:
            parse_context_line(
                file,
                line + i,
                document,
                keys,
                get_variable,
                line_text,
            )

    if len(keys) == 0:
        return None

    document.variables = list(variables.values())

    return document


def parse_context_line(
    file: str,
    line: int,
    document: SnippetDocument,
    keys: set[str],
    get_variable: Callable[[str], SnippetVariable],
    text: str,
):
    parts = text.split(":")

    if len(parts) != 2:
        error(file, line, f"Invalid line '{text}'")
        return

    key = parts[0].strip()
    value = parts[1].strip()

    if not key or not value:
        error(file, line, f"Invalid line '{text}'")
        return

    if key in keys:
        error(file, line, f"Duplicate key '{key}'")

    keys.add(key)

    match key:
        case "name":
            document.name = value
        case "description":
            document.description = value
        case "phrase":
            document.phrases = parse_vector_value(value)
        case "insertionScope":
            document.insertionScopes = parse_vector_value(value)
        case "language":
            document.languages = parse_vector_value(value)
        case _:
            if key.startswith("$"):
                parse_variable(file, line, get_variable, key, value)
            else:
                error(file, line, f"Invalid key '{key}'")


def parse_variable(
    file: str,
    line_numb: int,
    get_variable: Callable[[str], SnippetVariable],
    key: str,
    value: str,
):
    parts = key.split(".")

    if len(parts) != 2:
        error(file, line_numb, f"Invalid variable key '{key}'")
        return

    name = parts[0][1:]
    field = parts[1]

    match field:
        case "insertionFormatter":
            get_variable(name).insertion_formatters = parse_vector_value(value)
        case "wrapperPhrase":
            get_variable(name).wrapper_phrases = parse_vector_value(value)
        case "wrapperScope":
            get_variable(name).wrapper_scope = value
        case _:
            error(file, line_numb, f"Invalid variable key '{key}'")


def parse_body(text: str) -> Union[str, None]:
    # Find first line that is not empty. Preserve indentation.
    match_leading = re.search(r"^[ \t]*\S", text, flags=re.MULTILINE)

    if match_leading is None:
        return None

    return text[match_leading.start() :].rstrip()


def parse_vector_value(value: str) -> list[str]:
    return [v.strip() for v in value.split("|")]


def error(file: str, line: int, message: str):
    print(f"ERROR | {file}:{line+1} | {message}")
