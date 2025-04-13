from contextlib import suppress

from talon import Context, Module, actions, settings

from ..tags.operators import Operators

mod = Module()

ctx = Context()
ctx.matches = r"""
code.language: cpp
language: en
"""

mod.list("cpp_standard_functions", desc="Functions in the std namespace")
mod.list("cpp_standard_constants", desc="Constants in the std namespace")
mod.list("cpp_standard_types", desc="Types in the std namespace")
mod.list("cpp_namespace", desc="Commonly used namespaces")

ctx.lists["user.code_libraries"] = {
    "algorithm": "algorithm",
    "array": "array",
    "chrono": "chrono",
    "condition variable": "condition_variable",
    "deck": "deque",  # Pronounced "deck"
    "filesystem": "filesystem",
    "format": "format",
    "future": "future",
    "I O stream": "iostream",
    "list": "list",
    "map": "map",
    "mutex": "mutex",
    "optional": "optional",
    "queue": "queue",
    "regex": "regex",
    "set": "set",
    "stack": "stack",
    "string stream": "sstream",
    "string": "string",
    "thread": "thread",
    "tuple": "tuple",
    "unordered map": "unordered_map",
    "unordered set": "unordered_set",
    "variant": "variant",
    "vector": "vector",
}

ctx.lists["user.c_qualifiers"] = {
    "static": "static",
    "constant": "const",
    "const": "const",
    "volatile": "volatile",
    "extern": "extern",
    "const expert": "constexpr",
    "const expression": "constexpr",
    "constant expression": "constexpr",
}

ctx.lists["user.code_common_function"] = {
    "mem copy": "memcpy",
    "mem set": "memset",
    "print eff": "printf",
    "es print eff": "sprintf",
    "es en print eff": "sprintf",
    "ay to eye": "atoi",
    "size of": "sizeof",
    "exit": "exit",
}


@ctx.action_class("user")
class UserActions:
    def code_insert_null():
        actions.auto_insert("nullptr")

    def code_insert_is_null():
        actions.auto_insert(" == nullptr")

    def code_insert_is_not_null():
        actions.auto_insert(" != nullptr")
