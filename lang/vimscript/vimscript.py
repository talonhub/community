from talon import Context, Module, actions, settings

mod = Module()
ctx = Context()
ctx.lists["self.vimscript_functions"] = {
    "string len": "strlen",
    "get line": "getline",
    "set line": "setline",
    "length": "len",
}

ctx.lists["self.vimscript_scope"] = {
    "argument": "a:",
    "arg": "a:",
    "buffer": "b:",
    "buf": "b:",
    "window": "w:",
    "win": "w:",
    "tab": "t:",
    "special": "v:",
    "global": "g:",
    "local": "l:",
    "script local": "s:",
}

mod.list("vimscript_functions", desc="Standard built-in vimscript functions")
mod.list("vimscript_scope", desc="vimscript scoping types for functions and variables")


@mod.capture
def vimscript_functions(m) -> str:
    "Returns a string"


@mod.capture
def vimscript_scope(m) -> str:
    "Returns a string"


@ctx.capture(rule="{self.vimscript_functions}")
def vimscript_functions(m) -> str:
    return m.vimscript_functions


@ctx.capture(rule="{self.vimscript_scope}")
def vimscript_scope(m) -> str:
    return m.vimscript_scope
