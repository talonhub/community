# XXX - reorder some dicts for human readability so we see functions and libraries
# first

from talon import Context, Module, actions, settings

mod = Module()
mod.setting(
    "use_stdint_datatypes ", type=int, default=1, desc="beep",
)

ctx = Context()

ctx.lists["self.c_pointers"] = {
    "pointer": "*",
    "pointer to pointer": "**",
}

ctx.lists["self.stdint_signed"] = {
    "signed": "",
    "unsigned": "u",
}

ctx.lists["self.c_signed"] = {
    "signed": "signed ",
    "unsigned": "unsigned ",
}

common_types = {
    "static": "static",
    "volatile": "volatile",
    "register": "register",
}

ctx.lists["self.stdint_types"] = {
    "character": "int8_t",
    "char": "int8_t",
    "short": "int16_t",
    "long": "int32_t",
    "long long": "int64_t",
    "int": "int32_t",
    "integer": "int32_t",
    "void": "void",
    "double": "double",
    "struct": "struct",
    "struck": "struct",
    "num": "enum",
    "union": "union",
    "float": "float",
}

ctx.lists["self.c_types"] = {
    "character": "char",
    "char": "char",
    "short": "short",
    "long": "long",
    "int": "int",
    "integer": "int",
    "void": "void",
    "double": "double",
    "struct": "struct",
    "struck": "struct",
    "num": "enum",
    "union": "union",
    "float": "float",
}

ctx.lists["self.c_libraries"] = {
    "assert": "assert.h",
    "type": "ctype.h",
    "error": "errno.h",
    "float": "float.h",
    "limits": "limits.h",
    "locale": "locale.h",
    "math": "math.h",
    "set jump": "setjmp.h",
    "signal": "signal.h",
    "arguments": "stdarg.h",
    "definition": "stddef.h",
    "input": "stdio.h",
    "output": "stdio.h",
    "library": "stdlib.h",
    "string": "string.h",
    "time": "time.h",
    "standard int": "stdint.h",
}

ctx.lists["self.c_functions"] = {
    "mem copy": "memcpy",
    "mem set": "memset",
    "string cat": "strcat",
    "stir cat": "strcat",
    "stir en cat": "strncat",
    "stir elle cat": "strlcat",
    "stir copy": "strcpy",
    "stir en copy": "strncpy",
    "stir elle copy": "strlcpy",
    "string char": "strchr",
    "string dupe": "strdup",
    "stir dupe": "strdup",
    "stir comp": "strcmp",
    "stir en comp": "strncmp",
    "string len": "strlen",
    "stir len": "strlen",
    "is digit": "isdigit",
    "get char": "getchar",
    "print eff": "printf",
    "es print eff": "sprintf",
    "es en print eff": "sprintf",
    "stir to int": "strtoint",
    "stir to unsigned int": "strtouint",
    "ay to eye": "atoi",
    "em map": "mmap",
    "ma map": "mmap",
    "em un map": "munmap",
    "size of": "sizeof",
    "ef open": "fopen",
    "ef write": "fwrite",
    "ef read": "fread",
    "ef close": "fclose",
    "exit": "exit",
    "signal": "signal",
    "set jump": "setjmp",
    "get op": "getopt",
    "malloc": "malloc",
    "see alloc": "calloc",
    "alloc ah": "alloca",
    "re alloc": "realloc",
    "free": "free",
}

mod.list("c_pointers", desc="Common C pointers")
mod.list("c_signed", desc="Common C datatype signed modifiers")
mod.list("c_types", desc="Common C types")
mod.list("c_libraries", desc="Standard C library")
mod.list("c_functions", desc="Standard C functions")
mod.list("stdint_types", desc="Common stdint C types")
mod.list("stdint_signed", desc="Common stdint C datatype signed modifiers")


@mod.capture
def cast(m) -> str:
    "Returns a string"


@mod.capture
def stdint_cast(m) -> str:
    "Returns a string"


@mod.capture
def c_pointers(m) -> str:
    "Returns a string"


@mod.capture
def c_signed(m) -> str:
    "Returns a string"


@mod.capture
def c_types(m) -> str:
    "Returns a string"


@mod.capture
def c_functions(m) -> str:
    "Returns a string"


@mod.capture
def stdint_types(m) -> str:
    "Returns a string"


@mod.capture
def stdint_signed(m) -> str:
    "Returns a string"


@mod.capture
def variable(m) -> str:
    "Returns a string"


@mod.capture
def function(m) -> str:
    "Returns a string"


@mod.capture
def library(m) -> str:
    "Returns a string"


@ctx.capture(rule="{self.c_pointers}")
def c_pointers(m) -> str:
    return m.c_pointers


@ctx.capture(rule="{self.c_signed}")
def c_signed(m) -> str:
    return m.c_signed


@ctx.capture(rule="{self.c_types}")
def c_types(m) -> str:
    return m.c_types


@ctx.capture(rule="{self.c_types}")
def c_types(m) -> str:
    return m.c_types


@ctx.capture(rule="{self.c_functions}")
def c_functions(m) -> str:
    return m.c_functions


@ctx.capture(rule="{self.stdint_types}")
def stdint_types(m) -> str:
    return m.stdint_types


@ctx.capture(rule="{self.stdint_signed}")
def stdint_signed(m) -> str:
    return m.stdint_signed


@ctx.capture(rule="{self.c_libraries}")
def library(m) -> str:
    return m.c_libraries


# NOTE: we purposely we don't have a space after signed, to faciltate stdint
# style uint8_t constructions
@ctx.capture(rule="[<self.c_signed>]<self.c_types> [<self.c_pointers>+]")
def cast(m) -> str:
    return "(" + " ".join(list(m)) + ")"


# NOTE: we purposely we don't have a space after signed, to faciltate stdint
# style uint8_t constructions
@ctx.capture(rule="[<self.stdint_signed>]<self.stdint_types> [<self.c_pointers>+]")
def stdint_cast(m) -> str:
    return "(" + "".join(list(m)) + ")"


@ctx.capture(rule="[<self.c_signed>]<self.c_types>[<self.c_pointers>]")
def variable(m) -> str:
    return " ".join(list(m))
