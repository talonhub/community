import re
from collections.abc import Generator
from enum import Enum, auto
from typing import NamedTuple


class TokenType(Enum):
    OPTIONAL_START = auto()
    OPTIONAL_END = auto()
    ZERO_OR_MORE = auto()
    ONE_OR_MORE = auto()
    CHOICE = auto()
    GROUP_START = auto()
    GROUP_END = auto()
    LIST_START = auto()
    LIST_END = auto()
    CAPTURE_START = auto()
    CAPTURE_END = auto()
    START_ANCHOR = auto()
    END_ANCHOR = auto()
    WHITESPACE = auto()
    WORDS = auto()


TOKEN_SPECIFICATION = {
    TokenType.OPTIONAL_START: r"\[",
    TokenType.OPTIONAL_END: r"\]",
    TokenType.ZERO_OR_MORE: r"\*",
    TokenType.ONE_OR_MORE: r"\+",
    TokenType.CHOICE: r"\|",
    TokenType.GROUP_START: r"\(",
    TokenType.GROUP_END: r"\)",
    TokenType.LIST_START: r"\{",
    TokenType.LIST_END: r"\}",
    TokenType.CAPTURE_START: r"\<",
    TokenType.CAPTURE_END: r"\>",
    TokenType.START_ANCHOR: r"\^",
    TokenType.END_ANCHOR: r"\$",
    TokenType.WHITESPACE: r"\s",
    TokenType.WORDS: r"\w+",
}


class Token(NamedTuple):
    type: TokenType
    value: str
    column: int


TOKENIZE_REGEX = re.compile(
    "|".join(f"(?P<{token.name}>{TOKEN_SPECIFICATION[token]})" for token in TokenType)
)


def tokenize(input_string: str) -> Generator[Token]:
    for match in TOKENIZE_REGEX.finditer(input_string):
        if match.lastgroup is None:
            raise ValueError("Unexpected character in input string")
        kind = TokenType[match.lastgroup]
        if kind == TokenType.WHITESPACE:
            continue
        value = match.group()
        column = match.start()
        yield Token(type=kind, value=value, column=column)
