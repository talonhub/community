from user.pokey_talon.code.terms import SELECT, TELEPORT
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

mod.list("decorative_actions", desc="Supported actions for decorative navigation")
ctx.lists["self.decorative_actions"] = {
    SELECT: "decorative-navigation.selectToken",
    TELEPORT: "decorative-navigation.moveCursorBeforeToken",
    "post": "decorative-navigation.moveCursorAfterToken",
    "cursor": "decorative-navigation.addCursorAtToken",
}
