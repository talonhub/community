from talon import Context

ctx = Context()
ctx.matches = r"""
tag: user.rango_number_hints
"""


@ctx.capture("user.rango_hint", rule="<user.number_string>")
def rango_hint(m) -> str:
    return "".join(m)


@ctx.capture(
    "user.rango_list_hint_target",
    rule="<user.rango_primitive_hint_target> (plus <user.rango_primitive_hint_target>)+",
)
def rango_list_hint_target(m) -> dict:
    return {
        "type": "list",
        "items": m.rango_primitive_hint_target_list,
    }
