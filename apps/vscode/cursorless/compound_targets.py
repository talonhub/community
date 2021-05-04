import json
from .primitive_target import BASE_TARGET
from talon import Module

mod = Module()


@mod.capture(
    rule=(
        "<user.cursorless_primitive_target> | "
        "through <user.cursorless_primitive_target> | "
        "[range] <user.cursorless_primitive_target> through <user.cursorless_primitive_target>"
    )
)
def cursorless_range(m) -> str:
    if "through" in m:
        end = json.loads(m[-1])
        if m[0] == "through":
            start = BASE_TARGET.copy()
        else:
            start = json.loads(m.cursorless_primitive_target_list[0])
        return json.dumps(
            {
                "type": "range",
                "start": start,
                "end": end,
            }
        )

    return m[0]


@mod.capture(rule=("<user.cursorless_range> (and <user.cursorless_range>)*"))
def cursorless_target(m) -> str:
    if len(m.cursorless_range_list) == 1:
        return m.cursorless_range
    return json.dumps(
        {
            "type": "list",
            "elements": [json.loads(match) for match in m.cursorless_range_list],
        }
    )
