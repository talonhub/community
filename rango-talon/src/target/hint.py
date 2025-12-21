from talon import Module

mod = Module()


@mod.capture(rule="<user.letter> (twice | second)")
def rango_hint_double(m) -> str:
    return m.letter + m.letter


@mod.capture(
    rule="<user.letter> | <user.letter> <user.letter> | <user.rango_hint_double>"
)
def rango_hint(m) -> str:
    return "".join(m)
