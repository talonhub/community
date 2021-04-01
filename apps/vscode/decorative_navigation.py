from user.pokey_talon.code.terms import SELECT, TELEPORT, DELETE, FIND
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
    "bull": "red",
    "low": "yellow",
    "perp": "mauve",
}

mod.list("decorative_action", desc="Supported actions for decorative navigation")
ctx.lists["self.decorative_action"] = {
    # Accepts any single extent
    SELECT: "decorative-navigation.select",
    "cut": "decorative-navigation.cut",
    "copy": "decorative-navigation.copy",
    DELETE: "decorative-navigation.delete",
    FIND: "decorative-navigation.findInFile",
    f"{FIND} all": "decorative-navigation.findInFile",
    # Accepts any single extent, but behaviour different for lines?
    "use": "decorative-navigation.use",
    # Accepts only single token or line
    TELEPORT: "decorative-navigation.moveCursorBefore",
    "post": "decorative-navigation.moveCursorAfter",
    "cursor": "decorative-navigation.addCursorAt",
    f"{SELECT} past": "decorative-navigation.selectPast",
    f"{SELECT} till": "decorative-navigation.selectUntil",
    # Accepts only single token
    "rename": "decorative-navigation.rename",
    "ref show": "decorative-navigation.showReferences",
    "def show": "decorative-navigation.showDefinition",
    # Require 2 extents of any kind, but prob best to assume second extend is
    # same type as first, and need ot explicitly say "token" if you want to use
    # a token for the second one if the first is not
    # Note: these should actually be of the form "swap <range> with"
    "swap": "decorative-navigation.swap",
    "replace": "decorative-navigation.replace",
    # Require 1 extent of any kind, and 1 single token
    # Infers line vs token based on first extent type
    # Note: these should actually be of the form "use <range> after"
    "use after": "decorative-navigation.useAfter",
    "use before": "decorative-navigation.useBefore",
    "move after": "decorative-navigation.moveAfter",
    "move before": "decorative-navigation.moveBefore",
    # Require 1 extent of any kind, and 1 format string (eg "camel foo bar",
    # "phrase hello world" etc)
    # Note: these should actually be of the form "change <range> to"
    "change to": "decorative-navigation.changeTo",
    # Require 1 extent of any kind, and 1 format type (eg camel, uppercase,
    # phrase etc)
    # Note: these should actually be of the form "reformat <range> as"
    "reformat as": "decorative-navigation.reformatAs",
}


@mod.capture(rule="[{user.symbol_color}] <user.any_alphanumeric_key>")
def decorated_symbol(m) -> str:
    """A decorated symbol"""
    return str(m)


@mod.capture(
    rule=(
        "<user.decorated_symbol> | "
        "line <user.decorated_symbol> | "
        "range <user.decorated_symbol> through <user.decorated_symbol> | "
        "line range <user.decorated_symbol> through <user.decorated_symbol> | "
        "in {user.pair_symbol} at <user.decorated_symbol> | "
        "out {user.pair_symbol} at <user.decorated_symbol> | "
        "<user.decorated_symbol> <user.ordinals> |"
        "this | "
        "this line"
    )
)
def decorative_extent(m) -> str:
    """Supported extents for decorative navigation"""
    return str(m)