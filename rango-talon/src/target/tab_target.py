from talon import Module

mod = Module()


@mod.capture(rule="<user.letter> | <user.letter> <user.letter>")
def rango_tab_marker(m) -> str:
    return "".join(m)


@mod.capture(rule="<user.rango_tab_marker>")
def rango_primitive_tab_target(m) -> dict:
    return {
        "type": "primitive",
        "mark": {"type": "tabMarker", "value": m.rango_tab_marker},
    }


@mod.capture(
    rule="<user.rango_primitive_tab_target> (and <user.rango_primitive_tab_target>)+"
)
def rango_list_tab_target(m) -> dict:
    return {
        "type": "list",
        "items": m.rango_primitive_tab_target_list,
    }


@mod.capture(
    rule="<user.rango_primitive_tab_target> until <user.rango_primitive_tab_target>"
)
def rango_range_tab_target(m) -> dict:
    return {
        "type": "range",
        "anchor": m.rango_primitive_tab_target_1,
        "active": m.rango_primitive_tab_target_2,
    }


@mod.capture(
    rule="<user.rango_primitive_tab_target> | <user.rango_list_tab_target> | <user.rango_range_tab_target>"
)
def rango_tab_target(m) -> dict:
    return m[0]
