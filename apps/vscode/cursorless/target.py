from ....code.terms import SELECT, TELEPORT, DELETE, FIND

from enum import Enum
from dataclasses import dataclass
from ....code.keys import symbol_key_words
import json

from talon import Context, actions, ui, Module, app, clip

ctx = Context()
mod = Module()

ctx.matches = r"""
app: vscode
"""

mod.list("symbol_color", desc="Supported symbol colors for token jumping")
ctx.lists["self.symbol_color"] = {
    "gray": "default",
    "blue": "blue",
    "green": "green",
    "rose": "red",
    "squash": "yellow",
    "plum": "mauve",
}


CONNECTIVES = {"at", "of", "in", "containing"}

BASE_TARGET = {"type": "primitive"}


@mod.capture(
    rule=(
        "[{user.cursorless_position}] "
        "[{user.cursorless_selection_type} [of | in | containing]] "
        "[<user.cursorless_range_transformation>] "
        "[<user.cursorless_indexer> [at]]"
        "(<user.decorated_symbol> | {user.cursorless_mark} | {user.unmarked_core} | <user.cursorless_surrounding_pair> | <user.cursorless_indexer>)"
        "[<user.cursorless_indexer> | {user.cursorless_matching}]"
    )
)
def cursorless_target(m) -> str:
    """Supported extents for cursorless navigation"""
    object = BASE_TARGET.copy()
    for capture in m:
        if capture in CONNECTIVES:
            continue
        for key, value in json.loads(capture).items():
            if (
                key in object
                and key == SELECTION_TYPE_KEY
                and ranked_selection_types[value] < ranked_selection_types[object[key]]
            ):
                continue
            object[key] = value

    return json.dumps(object)


@dataclass
class ModifierTerm:
    term: str
    info: dict

    @property
    def value(self):
        return json.dumps(self.info)


def make_simple_transformation(type: str):
    return {"transformation": {"type": type}}


matching_transformation = ModifierTerm(
    "matching", make_simple_transformation("matchingPairSymbol")
)

mod.list("cursorless_matching", desc="Supported symbol extent types")
ctx.lists["self.cursorless_matching"] = {
    matching_transformation.term: matching_transformation.value
}

symbol_definition_type_map = {
    "funk": "function",
    "named funk": "namedFunction",
    "class": "class",
    "symbol": "symbol",
}

symbol_definition_types = {
    term: {
        "transformation": {
            "type": "containingSymbolDefinition",
            "symbolType": symbol_definition_type,
        }
    }
    for term, symbol_definition_type in symbol_definition_type_map.items()
}

mod.list("symbol_definition_type", desc="Supported symbol extent types")
ctx.lists["self.symbol_definition_type"] = {
    key: json.dumps(value) for key, value in symbol_definition_types.items()
}

SELECTION_TYPE_KEY = "selectionType"


@dataclass
class SelectionType:
    singular: str
    plural: str
    json_name: str
    rank: int

    @property
    def json_repr(self):
        return {SELECTION_TYPE_KEY: self.json_name}


TOKEN = SelectionType("token", "tokens", "token", 0)
LINE = SelectionType("line", "lines", "line", 1)
BLOCK = SelectionType("block", "blocks", "block", 2)

SELECTION_TYPES = [
    TOKEN,
    LINE,
    BLOCK,
]

ranked_selection_types = {
    selection_type.json_name: selection_type.rank for selection_type in SELECTION_TYPES
}

cursor_mark = {"mark": {"type": "cursor"}}

marks = {
    "here": cursor_mark,
    "this": cursor_mark,
    **{
        f"this {selection_type.singular}": {**selection_type.json_repr, **cursor_mark}
        for selection_type in SELECTION_TYPES
    },
    **{
        f"these {selection_type.plural}": {**selection_type.json_repr, **cursor_mark}
        for selection_type in SELECTION_TYPES
    },
    "change": {"mark": {"type": "lastEditRange"}},
    "last cursor": {"mark": {"type": "lastCursorPosition"}},
    **{
        f"this {symbol_definition_type}": {**cursor_mark, **value}
        for symbol_definition_type, value in symbol_definition_types.items()
    },
}

mod.list("cursorless_mark", desc="Types of marks")
ctx.lists["self.cursorless_mark"] = {
    key: json.dumps(value) for key, value in marks.items()
}

unmarked_cores = {
    **symbol_definition_types,
    **{
        selection_type.singular: selection_type.json_repr
        for selection_type in SELECTION_TYPES
    },
    matching_transformation.term: matching_transformation.info,
}

mod.list("unmarked_core", desc="Core terms whose mark must be inferred")
ctx.lists["self.unmarked_core"] = {
    key: json.dumps(value) for key, value in unmarked_cores.items()
}


positions = {
    "after": {"position": "after"},
    "before": {"position": "before"},
    "start of": {"position": "start"},
    "end of": {"position": "end"},
    "above": {"position": "before", **LINE.json_repr},
    "below": {"position": "after", **LINE.json_repr},
}

mod.list("cursorless_position", desc="Types of positions")
ctx.lists["self.cursorless_position"] = {
    key: json.dumps(value) for key, value in positions.items()
}

selection_type_map = {}

for selection_type in SELECTION_TYPES:
    selection_type_map[selection_type.singular] = selection_type.json_repr
    selection_type_map[selection_type.plural] = selection_type.json_repr

mod.list("cursorless_selection_type", desc="Types of selection_types")
ctx.lists["self.cursorless_selection_type"] = {
    key: json.dumps(value) for key, value in selection_type_map.items()
}


@mod.capture(rule="[at] [{user.symbol_color}] <user.any_alphanumeric_key>")
def decorated_symbol(m) -> str:
    """A decorated symbol"""
    try:
        symbol_color = m.symbol_color
    except AttributeError:
        symbol_color = "default"

    character = m.any_alphanumeric_key

    return json.dumps(
        {
            "mark": {
                "type": "decoratedSymbol",
                "symbolColor": symbol_color,
                "character": character,
            }
        }
    )


mod.list("cursorless_sub_component_type", desc="Supported subcomponent types")
ctx.lists["self.cursorless_sub_component_type"] = {
    "small": "subtoken",
    "subtoken": "subtoken",
    "subtokens": "subtoken",
    "subword": "subtoken",
    "subwords": "subtoken",
    "car": "character",
    "cars": "character",
    "character": "character",
    "characters": "character",
    "letter": "character",
    "letters": "character",
}


@mod.capture(
    rule=(
        "<user.ordinals> [through <user.ordinals>] {user.cursorless_sub_component_type}"
    )
)
def cursorless_indexer(m) -> str:
    """Supported extents for cursorless navigation"""
    return json.dumps(
        {
            "transformation": {
                "type": "subpiece",
                "pieceType": m.cursorless_sub_component_type,
                "startIndex": m.ordinals_list[0],
                "endIndex": m.ordinals_list[-1] + 1,
            }
        }
    )


pair_symbols = {
    "[": "squareBrackets",
    "]": "squareBrackets",
    "{": "curlyBrackets",
    "}": "curlyBrackets",
    "<": "angleBrackets",
    ">": "angleBrackets",
    "(": "parentheses",
    ")": "parentheses",
    '"': "doubleQuotes",
    "'": "singleQuotes",
}

mod.list("pair_symbol", desc="A pair symbol")
ctx.lists["self.pair_symbol"] = {
    phrase: pair_symbols[character]
    for phrase, character in symbol_key_words.items()
    if character in pair_symbols
}

cursorless_pair_surround_types = {
    "out": {"includePairDelimiter": True},
    "outer": {"includePairDelimiter": True},
    "outside": {"includePairDelimiter": True},
    "in": {"includePairDelimiter": False},
    "inner": {"includePairDelimiter": False},
    "inside": {"includePairDelimiter": False},
}

mod.list("cursorless_pair_surround_type", desc="Supported pair surround types")
ctx.lists["self.cursorless_pair_surround_type"] = {
    key: json.dumps(value) for key, value in cursorless_pair_surround_types.items()
}


@mod.capture(rule=("{user.cursorless_pair_surround_type} {user.pair_symbol}"))
def cursorless_surrounding_pair(m) -> str:
    """Supported extents for cursorless navigation"""
    return json.dumps(
        {
            "transformation": {
                "type": "surroundingPair",
                "delimiter": m.pair_symbol,
                **json.loads(m.cursorless_pair_surround_type),
            }
        }
    )


simple_transformations = [
    matching_transformation,
]

mod.list("cursorless_simple_transformations", desc="simple transformations")
ctx.lists["self.cursorless_simple_transformations"] = {
    transformation.term: transformation.value
    for transformation in simple_transformations
}


@mod.capture(rule=("[inside] {user.symbol_definition_type} [containing]"))
def cursorless_containing_symbol(m) -> str:
    """Supported extents for cursorless navigation"""
    if m[0] in ["inside"]:
        current_target = json.loads(m.symbol_definition_type)
        current_target["transformation"]["valueOnly"] = True
        return json.dumps(current_target)
    return m.symbol_definition_type


@mod.capture(
    rule=(
        "<user.cursorless_surrounding_pair> |"
        "{user.cursorless_simple_transformations} |"
        "<user.cursorless_containing_symbol>"
    )
)
def cursorless_range_transformation(m) -> str:
    """Supported positions for cursorless navigation"""
    return str(m)


"range <user.decorated_symbol> through <user.decorated_symbol> | "