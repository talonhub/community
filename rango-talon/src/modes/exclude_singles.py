from talon import Context

ctx = Context()

ctx.matches = r"""
tag: browser
and tag: user.rango_exclude_singles
"""


@ctx.capture("user.rango_hint", rule="<user.letter> <user.letter>")
def rango_hint(m) -> str:
    return "".join(m)
