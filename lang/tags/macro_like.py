from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.tag(
    "code_macro_like",
    desc="Enables macro-like language functionality",
)

# Java Annotations are grouped in w/ macros, even though they are fairly different functionality-wise
mod.list(
    "code_basic_macro_likes",
    desc="A list of single-line macro-likes without any parameters (ex: Swift's `@Observable`; Java's `@FunctionalInterface`)",
)
mod.list(
    "code_function_macro_likes",
    desc="A list of macro-likes which take parameters as if they were functions (ex: Rust's `print!`)",
)
mod.list(
    "code_array_macro_likes",
    desc="A list of macro-likes which take parameters as if they were arrays/lists (ex: Rust's `vec!`)",
)
mod.list(
    "code_block_macro_likes",
    desc="A list of macro-likes which take a code block as their (usually sole) parameter(s) (ex: Rust's `macro_rules!`)",
)

ctx.matches = r"""
tag: user.code_macro_like
"""

basic_macro_likes = {}
function_macro_likes = {}
array_macro_likes = {}
block_macro_likes = {}

ctx.lists["user.code_basic_macro_likes"] = basic_macro_likes
ctx.lists["user.code_function_macro_likes"] = function_macro_likes
ctx.lists["user.code_array_macro_likes"] = array_macro_likes
ctx.lists["user.code_block_macro_likes"] = block_macro_likes


# Direct clone of code_insert_function_or_macro implementation in rust.py
def do_macro_like_insert(text: str, selection: str, left_delim: str, right_delim: str):
    if selection:
        out_text = text + f"{left_delim}{selection}{right_delim}"
    else:
        out_text = text + f"{left_delim}{right_delim}"
    actions.user.paste(out_text)
    actions.edit.left()


@mod.capture(rule="{user.code_basic_macro_likes}")
def code_basic_macro_likes(m) -> str:
    "A basic macro-like"
    return m.code_basic_macro_likes


@mod.capture(rule="{code_function_macro_likes}")
def code_function_macro_likes(m) -> str:
    "A function-like macro-like"
    return m.code_function_macro_likes


@mod.capture(rule="{code_array_macro_likes}")
def code_array_macro_likes(m) -> str:
    "A array-like macro-like"
    return m.code_array_macro_likes


@mod.capture(rule="{code_block_macros_likes}")
def code_block_macros(m) -> str:
    "A block macro-like"
    return m.code_block_macros_likes


@mod.action_class
class Actions:
    def code_insert_basic_macro_like(text: str):
        """Insert a basic macro-like at the cursor."""
        actions.user.paste(text)

    def code_insert_function_macro_like(text: str, selection: str):
        """
        Insert a function-like annotation/macro and position the cursor appropriately.
        Overload this if the language does not use `()` as the function parameter delimiter pair.
        """
        do_macro_like_insert(text, selection, "(", ")")

    def code_insert_macro_array_like(text: str, selection: str):
        """
        Insert a array-like annotation/macro and position the cursor appropriately.
        Overload this if the language does not use `[]` as the array delimiter pair.
        """
        do_macro_like_insert(text, selection, "[", "]")

    def code_insert_macro_block_like(text: str, selection: str):
        """
        Insert a code block based annotation/macro and the cursor appropriately.
        Overload this if the language does not use `{}` as the array delimiter pair.
        """
        do_macro_like_insert(text, selection, "{", "}")
