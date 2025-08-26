import logging
import re
from copy import deepcopy
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


def create_snippets_from_file(file: Path) -> list[Snippet]:
    documents = parse_file(file)
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
    body = normalize_snippet_body_tabs(document.body)
    variables = combine_variables(default_context.variables, document.variables)

    snippet = Snippet(
        name=document.name or default_context.name or "",
        description=document.description or default_context.description,
        languages=document.languages or default_context.languages,
        phrases=document.phrases or default_context.phrases,
        insertion_scopes=document.insertionScopes or default_context.insertionScopes,
        variables=variables,
        body=body,
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
        if not is_variable_in_body(variable.name, snippet.body):
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


def is_variable_in_body(variable_name: str, body: str) -> bool:
    return (
        re.search(create_variable_regular_expression(variable_name), body) is not None
    )


def create_variable_regular_expression(variable_name: str) -> str:
    # $value or ${value} or ${value:default}
    # *? is used to find the smallest possible match.
    # This stops multiple stops from being treated as a single stop.
    return rf"\${variable_name}|\${{{variable_name}.*?}}"


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


def add_final_stop_to_snippet_body(body: str) -> str:
    """Make the snippet body end with stop $0 to allow exiting the snippet with `snip next`.
    If the snippet has a stop named `0`, it will get replaced with the largest number of a snippet variable name
    plus 1 with the original variable metadata for stop `0` now associated with the replacement.
    """
    if not body:
        return body

    final_stop_matches = find_variable_matches("0", body)
    # If there is already a final stop at the end, make no change
    if len(final_stop_matches) > 0 and final_stop_matches[-1].end() == len(body):
        return body

    biggest_variable_number: int | None = find_largest_variable_number(body)
    #If there is no integer variable, just add the final stop at the end
    if biggest_variable_number is None:
        return body + "$0"

    # If the biggest matching variable is at the end and there is no zero stop, make no change
    if len(final_stop_matches) == 0 and is_variable_last_match_at_end(
        str(biggest_variable_number), body
    ):
        return body

    #Add the final stop to the end but replace the original final stop
    replacement_name = str(biggest_variable_number + 1)
    return replace_final_stop(body, replacement_name, final_stop_matches) + "$0"


def is_variable_last_match_at_end(variable: str, body) -> bool:
    matches = find_variable_matches(variable, body)
    return len(matches) > 0 and matches[-1].end() == len(body)


def replace_final_stop(body: str, replacement_name: str, final_stop_matches) -> str:
    # Dealing with matches in reverse means replacing a match
    # does not change the location of the remaining matches.
    for match in reversed(final_stop_matches):
        replacement = match.group().replace("0", replacement_name, 1)
        body = body[: match.start()] + replacement + body[match.end() :]
    return body


def replace_variables_for_final_stop(variables, replacement_name: str):
    variables_clone = deepcopy(variables)
    for variable in variables_clone:
        if variable.name == "0":
            variable.name = replacement_name
    return variables_clone


def find_variable_matches(variable_name: str, body: str) -> list[re.Match[str]]:
    """Find every match of a variable in the body"""
    expression = create_variable_regular_expression(variable_name)
    matches = [m for m in re.finditer(expression, body)]
    return matches


def find_largest_variable_number(body: str) -> int | None:
    # Find all snippet stops with a numeric variable name
    # +? is used to find the smallest possible match.
    # We need this here to avoid treating multiple stops as a single one
    regular_expression = rf"\$\d+?|\${{\d+?:.*?}}|\${{\d+?}}"
    matches = re.findall(regular_expression, body)
    if matches:
        numbers = [
            compute_first_integer_in_string(match)
            for match in matches
            if match is not None
        ]
        if numbers:
            return max(numbers)
    return None


def compute_first_integer_in_string(text: str) -> int | None:
    start_index: int | None = None
    ending_index: int | None = None
    for i, char in enumerate(text):
        if char.isdigit():
            if start_index is None:
                start_index = i
            ending_index = i + 1
        elif start_index is not None:
            break
    if start_index is not None:
        integer_text = text[start_index:ending_index]
        return int(integer_text)
    return None


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


def parse_file(file: Path) -> list[SnippetDocument]:
    with open(file, encoding="utf-8") as f:
        content = f.read()
    return parse_file_content(file.name, content)


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
        warn(file, line, f"Duplicate key '{key}'")

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
                warn(file, line, f"Unknown key '{key}'")


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
            warn(file, line_numb, f"Unknown variable key '{key}'")


def parse_body(text: str) -> Union[str, None]:
    # Find first line that is not empty. Preserve indentation.
    match_leading = re.search(r"^[ \t]*\S", text, flags=re.MULTILINE)

    if match_leading is None:
        return None

    return text[match_leading.start() :].rstrip()


def parse_vector_value(value: str) -> list[str]:
    return [v.strip() for v in value.split("|")]


def error(file: str, line: int, message: str):
    logging.error(f"{file}:{line+1} | {message}")


def warn(file: str, line: int, message: str):
    logging.warning(f"{file}:{line+1} | {message}")
