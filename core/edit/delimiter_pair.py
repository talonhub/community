from talon import Module, actions

mod = Module()

mod.list("delimiter_pair", "List of matching pair delimiters")


@mod.capture(rule="{user.delimiter_pair}")
def delimiter_pair(m) -> list[str]:
    pair = m.delimiter_pair.split()
    assert len(pair) == 2
    # "space" requires a special written form because Talon lists are whitespace insensitive
    open = pair[0] if pair[0] != "space" else " "
    close = pair[1] if pair[1] != "space" else " "
    return [open, close]


@mod.action_class
class Actions:
    def delimiter_pair_insert(pair: list[str]):
        """Insert a delimiter pair <pair> leaving the cursor in the middle"""
        actions.user.insert_between(pair[0], pair[1])

    def delimiter_pair_wrap_selection(pair: list[str]):
        """Wrap selection with delimiter pair <pair>"""
        selected = actions.edit.selected_text()
        actions.insert(f"{pair[0]}{selected}{pair[1]}")
