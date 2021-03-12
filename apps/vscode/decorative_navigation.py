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
