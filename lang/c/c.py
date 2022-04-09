from talon import Context, Module, actions, settings

mod = Module()
mod.setting(
    "use_stdint_datatypes ",
    type=int,
    default=1,
    desc="Use the stdint datatype naming in commands by default",
)

ctx = Context()
ctx.matches = r"""
tag: user.c
"""

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

ctx.lists["self.c_keywords"] = {
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

ctx.lists["user.code_libraries"] = {
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

ctx.lists["user.code_common_function"] = {
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
mod.list("c_keywords", desc="C keywords")
mod.list("c_types", desc="Common C types")
mod.list("stdint_types", desc="Common stdint C types")
mod.list("stdint_signed", desc="Common stdint C datatype signed modifiers")


@mod.capture(rule="{self.c_pointers}")
def c_pointers(m) -> str:
    "Returns a string"
    return m.c_pointers


@mod.capture(rule="{self.c_signed}")
def c_signed(m) -> str:
    "Returns a string"
    return m.c_signed

@mod.capture(rule="{self.c_keywords}")
def c_keywords(m) -> str:
    "Returns a string"
    return m.c_keywords

@mod.capture(rule="{self.c_types}")
def c_types(m) -> str:
    "Returns a string"
    return m.c_types


@mod.capture(rule="{self.c_types}")
def c_types(m) -> str:
    "Returns a string"
    return m.c_types


@mod.capture(rule="{self.stdint_types}")
def stdint_types(m) -> str:
    "Returns a string"
    return m.stdint_types


@mod.capture(rule="{self.stdint_signed}")
def stdint_signed(m) -> str:
    "Returns a string"
    return m.stdint_signed


# NOTE: we purposely we don't have a space after signed, to faciltate stdint
# style uint8_t constructions
@mod.capture(rule="[<self.c_signed>]<self.c_types> [<self.c_pointers>+]")
def c_cast(m) -> str:
    "Returns a string"
    return "(" + " ".join(list(m)) + ")"


# NOTE: we purposely we don't have a space after signed, to faciltate stdint
# style uint8_t constructions
@mod.capture(rule="[<self.stdint_signed>]<self.stdint_types> [<self.c_pointers>+]")
def c_stdint_cast(m) -> str:
    "Returns a string"
    return "(" + "".join(list(m)) + ")"


@mod.capture(rule="[<self.c_signed>]<self.c_types>[<self.c_pointers>]")
def c_variable(m) -> str:
    "Returns a string"
    return " ".join(list(m))


@ctx.action_class("user")
class UserActions:
    def code_operator_indirection():           actions.auto_insert('*')
    def code_operator_address_of():            actions.auto_insert('&')
    def code_operator_structure_dereference(): actions.auto_insert('->')
    def code_operator_subscript():
        actions.insert('[]')
        actions.key('left')
    def code_operator_assignment():                      actions.auto_insert(' = ')
    def code_operator_subtraction():                     actions.auto_insert(' - ')
    def code_operator_subtraction_assignment():          actions.auto_insert(' -= ')
    def code_operator_addition():                        actions.auto_insert(' + ')
    def code_operator_addition_assignment():             actions.auto_insert(' += ')
    def code_operator_multiplication():                  actions.auto_insert(' * ')
    def code_operator_multiplication_assignment():       actions.auto_insert(' *= ')
    #action(user.code_operator_exponent): " ** "
    def code_operator_division():                        actions.auto_insert(' / ')
    def code_operator_division_assignment():             actions.auto_insert(' /= ')
    def code_operator_modulo():                          actions.auto_insert(' % ')
    def code_operator_modulo_assignment():               actions.auto_insert(' %= ')
    def code_operator_equal():                           actions.auto_insert(' == ')
    def code_operator_not_equal():                       actions.auto_insert(' != ')
    def code_operator_greater_than():                    actions.auto_insert(' > ')
    def code_operator_greater_than_or_equal_to():        actions.auto_insert(' >= ')
    def code_operator_less_than():                       actions.auto_insert(' < ')
    def code_operator_less_than_or_equal_to():           actions.auto_insert(' <= ')
    def code_operator_and():                             actions.auto_insert(' && ')
    def code_operator_or():                              actions.auto_insert(' || ')
    def code_operator_bitwise_and():                     actions.auto_insert(' & ')
    def code_operator_bitwise_and_assignment():          actions.auto_insert(' &= ')
    def code_operator_bitwise_or():                      actions.auto_insert(' | ')
    def code_operator_bitwise_or_assignment():           actions.auto_insert(' |= ')
    def code_operator_bitwise_exclusive_or():            actions.auto_insert(' ^ ')
    def code_operator_bitwise_exclusive_or_assignment(): actions.auto_insert(' ^= ')
    def code_operator_bitwise_left_shift():              actions.auto_insert(' << ')
    def code_operator_bitwise_left_shift_assignment():   actions.auto_insert(' <<= ')
    def code_operator_bitwise_right_shift():             actions.auto_insert(' >> ')
    def code_operator_bitwise_right_shift_assignment():  actions.auto_insert(' >>= ')
    def code_insert_null():                                     actions.auto_insert('NULL')
    def code_insert_is_null():                                  actions.auto_insert(' == NULL ')
    def code_insert_is_not_null():                              actions.auto_insert(' != NULL')
    def code_state_if():
        actions.insert('if () {\n}\n')
        actions.key('up:2 left:3')
    def code_state_else_if():
        actions.insert('else if () {\n}\n')
        actions.key('up:2 left:3')
    def code_state_else():
        actions.insert('else\n{\n}\n')
        actions.key('up:2')
    def code_state_switch():
        actions.insert('switch ()')
        actions.edit.left()
    def code_state_case():
        actions.insert('case \nbreak;')
        actions.edit.up()
    def code_state_for():   actions.auto_insert('for ')
    def code_state_go_to(): actions.auto_insert('goto ')
    def code_state_while():
        actions.insert('while ()')
        actions.edit.left()
    def code_state_return():    actions.auto_insert('return ')
    def code_break():           actions.auto_insert('break;')
    def code_next():            actions.auto_insert('continue;')
    def code_insert_true():            actions.auto_insert('true')
    def code_insert_false():           actions.auto_insert('false')
    def code_comment_line_prefix(): actions.auto_insert('//')

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()

    # TODO - it would be nice that you integrate that types from c_cast
    # instead of defaulting to void
    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_private_static_function(text: str):
        """Inserts private static function"""
        result = "static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_insert_library(text: str, selection: str):
        actions.user.paste("include <{}>".format(selection))
