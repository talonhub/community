from user.pokey_talon.code.terms import SELECT, TELEPORT, DELETE, FIND
from enum import Enum
from dataclasses import dataclass
from user.pokey_talon.code.keys import symbol_key_words
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

# TODO A lot of these could be supported by supporting a proper "pop back"
# Would basically use the same logic that is used for updating token ranges
mod.list("decorative_action", desc="Supported actions for decorative navigation")
ctx.lists["self.decorative_action"] = {
    # Accepts any single extent
    SELECT: "decorative-navigation.select",
    "cut": "decorative-navigation.cut",
    "copy": "decorative-navigation.copy",
    DELETE: "decorative-navigation.delete",
    FIND: "decorative-navigation.findInFile",
    f"{FIND} last": "decorative-navigation.findBackwardsInFile",
    f"{FIND} all": "decorative-navigation.findAll",
    "fold": "decorative-navigation.fold",
    # Accepts only single token or line
    TELEPORT: "decorative-navigation.moveCursorBefore",
    "post": "decorative-navigation.moveCursorAfter",
    "cursor": "decorative-navigation.addCursorAt",
    "cursor all": "decorative-navigation.addCursorToAllLines",
    f"{SELECT} past": "decorative-navigation.selectPast",
    f"{SELECT} till": "decorative-navigation.selectUntil",
    "phones": "phones",
    # Accepts only single token
    "rename": "decorative-navigation.rename",
    "ref show": "decorative-navigation.showReferences",
    "def show": "decorative-navigation.showDefinition",
    "hover show": "decorative-navigation.showHover",
    "act up": "decorative-navigation.scrollToTop",
    "act eat": "decorative-navigation.scrollToMid",
    "act down": "decorative-navigation.scrollToBottom",
    # Require 2 extents of any kind, but prob best to assume second extend is
    # same type as first, and need to explicitly say "token" if you want to use
    # a token for the second one if the first is not
    # Note: these should actually be of the form "swap <range> with"
    "swap": "decorative-navigation.swap",
    # Require 1 extent of any kind and 1 position, but prob best to assume
    # the position is same type as extent, and need to explicitly say "token"
    # if you want to use a token for the second one if the first is not
    "use": "decorative-navigation.use",
    # Require 1 extent of any kind, and 1 format string (eg "camel foo bar",
    # "phrase hello world" etc, "spell air bat cap")
    # Note: these should actually be of the form "replace <range> with"
    # Could also except a second extent, and that would replace it with that
    # extent
    "replace with": "decorative-navigation.replaceWith",
    # Require 1 extent of any kind, and 1 format type (eg camel, uppercase,
    # phrase etc)
    # Note: these should actually be of the form "reformat <range> as"
    "reformat as": "decorative-navigation.reformatAs",
    # Accepts position
    "paste": "decorative-navigation.paste",
}
"<user.search_engine>"

CONNECTIVES = ["at", "of", "in", "containing"]


@mod.capture(
    rule=(
        "[{user.decorative_position}] "
        "[{user.decorative_selection_type} [of | in | containing]] "
        "[<user.decorated_range_transformation>] "
        "(<user.decorated_symbol> | {user.decorative_mark})"
        "[<user.decorative_indexer> | {user.decorative_matching}]"
    )
)
def decorative_target(m) -> str:
    """Supported extents for decorative navigation"""
    object = {}
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
    "matching", make_simple_transformation("matching")
)

mod.list("decorative_matching", desc="Supported symbol extent types")
ctx.lists["self.decorative_matching"] = {
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

mod.list("decorative_mark", desc="Types of marks")
ctx.lists["self.decorative_mark"] = {
    key: json.dumps(value) for key, value in marks.items()
}


positions = {
    "after": {"position": "after"},
    "before": {"position": "before"},
    "start of": {"position": "start"},
    "end of": {"position": "end"},
    "above": {"position": "before", **LINE.json_repr},
    "below": {"position": "after", **LINE.json_repr},
}

mod.list("decorative_position", desc="Types of positions")
ctx.lists["self.decorative_position"] = {
    key: json.dumps(value) for key, value in positions.items()
}

selection_type_map = {}

for selection_type in SELECTION_TYPES:
    selection_type_map[selection_type.singular] = selection_type.json_repr
    selection_type_map[selection_type.plural] = selection_type.json_repr

mod.list("decorative_selection_type", desc="Types of selection_types")
ctx.lists["self.decorative_selection_type"] = {
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


mod.list("decorative_sub_component_type", desc="Supported subcomponent types")
ctx.lists["self.decorative_sub_component_type"] = {
    "small": "subtoken",
    "subtoken": "subtoken",
    "subword": "subtoken",
    "car": "character",
    "letter": "character",
}


@mod.capture(rule=("<user.ordinals> {user.decorative_sub_component_type}"))
def decorative_indexer(m) -> str:
    """Supported extents for decorative navigation"""
    return json.dumps(
        {
            "transformation": {
                "type": "subpiece",
                "pieceType": m.decorative_sub_component_type,
                "index": m.ordinals,
            }
        }
    )


pair_symbols = {
    "[": "squareBrackets",
    "]": "squareBrackets",
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

decorative_pair_surround_types = {
    "out": {"includePairDelimiter": True},
    "outer": {"includePairDelimiter": True},
    "outside": {"includePairDelimiter": True},
    "in": {"includePairDelimiter": False},
    "inner": {"includePairDelimiter": False},
    "inside": {"includePairDelimiter": False},
}

mod.list("decorative_pair_surround_type", desc="Supported pair surround types")
ctx.lists["self.decorative_pair_surround_type"] = {
    key: json.dumps(value) for key, value in decorative_pair_surround_types.items()
}


@mod.capture(rule=("{user.decorative_pair_surround_type} {user.pair_symbol}"))
def decorative_surrounding_pair(m) -> str:
    """Supported extents for decorative navigation"""
    return json.dumps(
        {
            "transformation": {
                "type": "surroundingPair",
                "delimiter": m.pair_symbol,
                **json.loads(m.decorative_pair_surround_type),
            }
        }
    )


simple_transformations = [
    matching_transformation,
]

mod.list("decorative_simple_transformations", desc="simple transformations")
ctx.lists["self.decorative_simple_transformations"] = {
    transformation.term: transformation.value
    for transformation in simple_transformations
}


@mod.capture(rule=("{user.symbol_definition_type} [containing]"))
def decorative_containing_symbol(m) -> str:
    """Supported extents for decorative navigation"""
    return m.symbol_definition_type


@mod.capture(
    rule=(
        "<user.decorative_surrounding_pair> |"
        "{user.decorative_simple_transformations} |"
        "<user.decorative_containing_symbol>"
    )
)
def decorated_range_transformation(m) -> str:
    """Supported positions for decorative navigation"""
    return str(m)


"range <user.decorated_symbol> through <user.decorated_symbol> | "