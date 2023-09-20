from talon import Context, Module

mod = Module()

ctx = Context()
ctx.matches = r"""
code.language: protobuf
"""

ctx.lists["user.code_type"] = {
    "string": "string",
    "bytes": "bytes",
    "you sixty four": "uint64",
    "you thirty two": "uint32",
    "eye sixty four": "int64",
    "eye thirty two": "int32",
    "sin sixty four": "sint64",
    "sin thirty two": "sint32",
    "fixed sixty four": "fixed64",
    "fixed thirty two": "fixed32",
    "as fixed sixty four": "sfixed64",
    "as fixed thirty two": "sfixed32",
    "boolean": "bool",
    "double": "double",
    "float": "float",
}
