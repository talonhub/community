from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.tag(
    "code_macro_like",
    desc="Enables macro-like language functionality",
)

# Java Annotations are grouped in w/ macros, even though they are fairly different functionality-wise
mod.list(
    "code_basic_macro_like",
    desc="A list of single-line macro-likes without any parameters (ex: Swift's `@Observable`; Java's `@FunctionalInterface`)",
)
mod.list(
    "code_function_macro_like",
    desc="A list of macro-likes which take parameters as if they were functions (ex: Rust's `print!`)",
)
mod.list(
    "code_array_macro_like",
    desc="A list of macro-likes which take parameters as if they were arrays/lists (ex: Rust's `vec!`)",
)
mod.list(
    "code_block_macro_like",
    desc="A list of macro-likes which take a code block as their (usually sole) parameter(s) (ex: Rust's `macro_rules!`)",
)

ctx.matches = r"""
tag: user.code_macro_like
"""

ctx.lists["user.code_basic_macro_like"] = {}
ctx.lists["user.code_function_macro_like"] = {}
ctx.lists["user.code_array_macro_like"] = {}
ctx.lists["user.code_block_macro_like"] = {}


# Direct clone of code_insert_function_or_macro formally implemented in rust.py
def do_macro_like_insert(text: str, selection: str, left_delim: str, right_delim: str):
    if selection:
        out_text = text + f"{left_delim}{selection}{right_delim}"
    else:
        out_text = text + f"{left_delim}{right_delim}"
    actions.user.paste(out_text)
    actions.edit.left()


def do_macro_like_meta(text: str, selection: str):
    basic = set(
        actions.user.talon_get_active_registry_list(
            "user.code_basic_macro_like"
        ).values()
    )
    func = set(
        actions.user.talon_get_active_registry_list(
            "user.code_function_macro_like"
        ).values()
    )
    array = set(
        actions.user.talon_get_active_registry_list(
            "user.code_array_macro_like"
        ).values()
    )
    block = set(
        actions.user.talon_get_active_registry_list(
            "user.code_block_macro_like"
        ).values()
    )
    if text in basic:
        actions.user.paste(text)
    elif text in func:
        do_macro_like_insert(text, selection, "(", ")")
    elif text in array:
        do_macro_like_insert(text, selection, "[", "]")
    elif text in block:
        do_macro_like_insert(text, selection, "{", "}")
    else:
        actions.app.notify(
            f"Macro-like {text} is in the all macro-likes capture, but is not in a macro-like variant list! Falling back on basic variant behavior...",
            "Macro-Like warning",
        )
        actions.user.paste(text)


@mod.capture(
    rule="{user.code_basic_macro_like} | {user.code_function_macro_like} | {user.code_array_macro_like} | {user.code_block_macro_like}"
)
def code_all_macro_like(m) -> str:
    return m[0]


@mod.action_class
class Actions:
    def code_insert_macro_like(text: str, selection: str):
        """Inserts a macro-like, positioning the cursor appropriately"""
        do_macro_like_meta(text, selection)
