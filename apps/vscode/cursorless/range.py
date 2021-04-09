import json
from .target import cursor_mark
from talon import Context, actions, ui, Module, app, clip

mod = Module()


def make_position(position):
    return {
        "type": "position",
        "target": position,
    }


@mod.capture(
    rule=(
        "<user.cursorless_target> | "
        "through <user.cursorless_target> | "
        "[range] <user.cursorless_target> through <user.cursorless_target>"
    )
)
def cursorless_range(m) -> str:
    if "through" in m:
        end = json.loads(m[-1])
        if m[0] == "through":
            start = cursor_mark
        else:
            start = json.loads(m.cursorless_target_list[0])
        return json.dumps(
            {
                "type": "range",
                "start": make_position(start),
                "end": make_position(end),
            }
        )

    return json.dumps(make_position(json.loads(m[0])))


@mod.capture(rule=("<user.cursorless_range> (and <user.cursorless_range>)*"))
def cursorless_arg(m) -> str:
    if len(m.cursorless_range_list) == 1:
        return m.cursorless_range
    return json.dumps(
        {
            "type": "list",
            "elements": [json.loads(match) for match in m.cursorless_range_list],
        }
    )
