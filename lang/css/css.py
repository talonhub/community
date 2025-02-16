from talon import Context, Module, actions

from ..tags.operators import Operators

mod = Module()
global_ctx = Context()
ctx = Context()
ctx.matches = """
code.language: css
code.language: scss
"""

mod.list("css_at_rule", desc="List of CSS @rules")
mod.list("css_unit", desc="List of CSS units")
mod.list("css_global_value", desc="CSS-wide values")

global_ctx.lists["self.css_unit"] = {
    # distance (length)
    "char": "ch",
    "em": "em",
    "rem": "rem",
    "pixels": "px",
    "points": "pt",
    "view height": "vh",
    "view width": "vw",
    # angle
    "degrees": "deg",
    "radians": "rad",
    "turn": "turn",
    # duration (time)
    "seconds": "s",
    "millis": "ms",
    # resolution
    "dots per pixel": "dppx",
    # flexible length (flex) - grid
    "fraction": "fr",
}

global_ctx.lists["self.css_at_rule"] = {
    # regular
    "charset": "charset",
    "import": "import",
    "namespace": "namespace",
    # conditional group
    "media": "media",
    "supports": "supports",
    # other nested
    "page": "page",
    "font face": "font-face",
    "keyframes": "keyframes",
    # CSS Modules
    "value": "value",
}

global_ctx.lists["self.css_global_value"] = ["initial", "inherit", "unset", "revert"]

ctx.lists["user.code_common_function"] = {
    # reference
    "attribute": "attr",
    "env": "env",
    "url": "url",
    "var": "var",
    "variable": "var",
    # mathematical
    "calc": "calc",
    "calculate": "calc",
    "clamp": "clamp",
    "max": "max",
    "min": "min",
    # color
    "HSL": "hsl",
    "hue sat light": "hsl",
    "HSLA": "hsla",
    "lab": "lab",
    "LCH": "lch",
    "RGB": "rgb",
    "red green blue": "rgb",
    "RGBA": "rgba",
    "color": "color",
    # image functions
    "linear gradient": "linear-gradient",
    # counter functions
    "counter": "counter",
    "counters": "counters",
    "symbols": "symbols",
    # filter
    "blur": "blur",
    "brightness": "brightness",
    "contrast": "contrast",
    "drop shadow": "drop-shadow",
    "grayscale": "grayscale",
    "hue rotate": "hue-rotate",
    "invert": "invert",
    "opacity": "opacity",
    "saturate": "saturate",
    "sepia": "sepia",
    # grid
    "fit content": "fit-content",
    "min max": "minmax",
    "repeat": "repeat",
    # transform
    "matrix": "matrix",
    "rotate": "rotate",
    "scale": "scale",
    "skew": "skew",
    "translate": "translate",
}

operators = Operators(
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_AND=" and ",
    MATH_OR=" or ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_import():
        actions.insert("@import ")

    def code_insert_function(text: str, selection: str):
        actions.user.paste(f"{text}({selection})")
        actions.edit.left()
