from talon import Module

mod = Module()


@mod.capture(rule="<user.rango_hint>")
def rango_primitive_hint_target(m) -> dict:
    return {
        "type": "primitive",
        "mark": {"type": "elementHint", "value": m.rango_hint},
    }


@mod.capture(
    rule="<user.rango_primitive_hint_target> (and <user.rango_primitive_hint_target>)+"
)
def rango_list_hint_target(m) -> dict:
    return {
        "type": "list",
        "items": m.rango_primitive_hint_target_list,
    }


@mod.capture(
    rule="<user.rango_primitive_hint_target> until <user.rango_primitive_hint_target>"
)
def rango_range_hint_target(m) -> dict:
    return {
        "type": "range",
        "anchor": m.rango_primitive_hint_target_1,
        "active": m.rango_primitive_hint_target_2,
    }


@mod.capture(
    rule="<user.rango_primitive_hint_target> | <user.rango_list_hint_target> | <user.rango_range_hint_target>"
)
def rango_direct_clicking_target(m) -> dict:
    return m[0]


@mod.capture(rule="mark <user.text>")
def rango_primitive_reference_target(m) -> dict:
    return {
        "type": "primitive",
        "mark": {"type": "elementReference", "value": m.text},
    }


@mod.capture(rule="text <user.text>")
def rango_primitive_text_target(m) -> dict:
    return {
        "type": "primitive",
        "mark": {
            "type": "textSearch",
            "value": m.text,
            "viewportOnly": True,
        },
    }


@mod.capture(
    rule="<user.rango_primitive_hint_target> | <user.rango_primitive_reference_target> | <user.rango_primitive_text_target>"
)
def rango_primitive_target(m) -> dict:
    return m[0]


@mod.capture(rule="<user.rango_primitive_target> (and <user.rango_primitive_target>)+")
def rango_list_target(m) -> dict:
    return {
        "type": "list",
        "items": m.rango_primitive_target_list,
    }


@mod.capture(rule="<user.rango_primitive_target> until <user.rango_primitive_target>")
def rango_range_target(m) -> dict:
    return {
        "type": "range",
        "anchor": m.rango_primitive_target_1,
        "active": m.rango_primitive_target_2,
    }


@mod.capture(
    rule="<user.rango_primitive_target> | <user.rango_list_target> | <user.rango_range_target>"
)
def rango_target(m) -> dict:
    return m[0]
