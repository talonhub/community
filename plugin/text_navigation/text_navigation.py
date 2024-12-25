import itertools
import re

from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()


mod.setting(
    "text_navigation_max_line_search",
    type=int,
    default=10,
    desc="The maximum number of rows that will be included in the search for the keywords above and below in <user direction>",
)

mod.list(
    "navigation_action",
    desc="Actions to perform, for instance move, select, cut, etc",
)
mod.list(
    "before_or_after",
    desc="Words to indicate if the cursor should be moved before or after a given reference point",
)
mod.list(
    "navigation_target_name",
    desc="Names for regular expressions for common things to navigate to, for instance a word with or without underscores",
)

navigation_target_names = {
    "word": r"\w+",
    "small": r"[A-Z]?[a-z0-9]+",
    "big": r"[\S]+",
    "parens": r"\((.*?)\)",
    "squares": r"\[(.*?)\]",
    "braces": r"\{(.*?)\}",
    "quotes": r"\"(.*?)\"",
    "angles": r"\<(.*?)\>",
    # "single quotes": r'\'(.*?)\'',
    "all": r"(.+)",
    "method": r"\w+\((.*?)\)",
    "constant": r"[A-Z_][A-Z_]+",
}
ctx.lists["self.navigation_target_name"] = navigation_target_names


@mod.capture(
    rule="<user.any_alphanumeric_key> | {user.navigation_target_name} | phrase <user.text>"
)
def navigation_target(m) -> re.Pattern:
    """A target to navigate to. Returns a regular expression."""
    if hasattr(m, "any_alphanumeric_key"):
        return re.compile(re.escape(m.any_alphanumeric_key), re.IGNORECASE)
    if hasattr(m, "navigation_target_name"):
        return re.compile(m.navigation_target_name)
    return re.compile(re.escape(m.text), re.IGNORECASE)


@mod.action_class
class Actions:
    def navigation(
        navigation_action: str,  # GO, EXTEND, SELECT, DELETE, CUT, COPY
        direction: str,  # up, down, left, right
        navigation_target_name: str,
        before_or_after: str,  # BEFORE, AFTER, DEFAULT
        regex: re.Pattern,
        occurrence_number: int,
    ):
        """Navigate in `direction` to the occurrence_number-th time that `regex` occurs, then execute `navigation_action` at the given `before_or_after` position."""
        direction = direction.upper()
        navigation_target_name = re.compile(
            navigation_target_names["word"]
            if (navigation_target_name == "DEFAULT")
            else navigation_target_name
        )
        function = navigate_left if direction in ("UP", "LEFT") else navigate_right
        function(
            navigation_action,
            navigation_target_name,
            before_or_after,
            regex,
            occurrence_number,
            direction,
        )

    def navigation_by_name(
        navigation_action: str,  # GO, EXTEND, SELECT, DELETE, CUT, COPY
        direction: str,  # up, down, left, right
        before_or_after: str,  # BEFORE, AFTER, DEFAULT
        navigation_target_name: str,  # word, big, small
        occurrence_number: int,
    ):
        """Like user.navigation, but to a named target."""
        r = re.compile(navigation_target_names[navigation_target_name])
        actions.user.navigation(
            navigation_action,
            direction,
            "DEFAULT",
            before_or_after,
            r,
            occurrence_number,
        )


def get_text_left():
    actions.edit.extend_line_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text


def get_text_right():
    actions.edit.extend_line_end()
    text = actions.edit.selected_text()
    actions.edit.left()
    return text


def get_text_up():
    actions.edit.up()
    actions.edit.line_end()
    for j in range(0, settings.get("user.text_navigation_max_line_search")):
        actions.edit.extend_up()
    actions.edit.extend_line_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text


def get_text_down():
    actions.edit.down()
    actions.edit.line_start()
    for j in range(0, settings.get("user.text_navigation_max_line_search")):
        actions.edit.extend_down()
    actions.edit.extend_line_end()
    text = actions.edit.selected_text()
    actions.edit.left()
    return text


def get_current_selection_size():
    return len(actions.edit.selected_text())


def go_right(i):
    for j in range(0, i):
        actions.edit.right()


def go_left(i):
    for j in range(0, i):
        actions.edit.left()


def extend_left(i):
    for j in range(0, i):
        actions.edit.extend_left()


def extend_right(i):
    for j in range(0, i):
        actions.edit.extend_right()


def select(direction, start, end, length):
    if direction == "RIGHT" or direction == "DOWN":
        go_right(start)
        extend_right(end - start)
    else:
        go_left(length - end)
        extend_left(end - start)


def navigate_left(
    navigation_action,
    navigation_target_name,
    before_or_after,
    regex,
    occurrence_number,
    direction,
):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0:
        actions.edit.right()
    text = get_text_left() if direction == "LEFT" else get_text_up()
    # only search in the text that was not selected
    subtext = (
        text if current_selection_length <= 0 else text[:-current_selection_length]
    )
    match = match_backwards(regex, occurrence_number, subtext)
    if match is None:
        # put back the old selection, if the search failed
        extend_left(current_selection_length)
        return
    start = match.start()
    end = match.end()
    handle_navigation_action(
        navigation_action,
        navigation_target_name,
        before_or_after,
        direction,
        text,
        start,
        end,
    )


def navigate_right(
    navigation_action,
    navigation_target_name,
    before_or_after,
    regex,
    occurrence_number,
    direction,
):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0:
        actions.edit.left()
    text = get_text_right() if direction == "RIGHT" else get_text_down()
    # only search in the text that was not selected
    sub_text = text[current_selection_length:]
    # pick the next interrater, Skip n number of occurrences, get an iterator given the Regex
    match = match_forward(regex, occurrence_number, sub_text)
    if match is None:
        # put back the old selection, if the search failed
        extend_right(current_selection_length)
        return
    start = current_selection_length + match.start()
    end = current_selection_length + match.end()
    handle_navigation_action(
        navigation_action,
        navigation_target_name,
        before_or_after,
        direction,
        text,
        start,
        end,
    )


def handle_navigation_action(
    navigation_action,
    navigation_target_name,
    before_or_after,
    direction,
    text,
    start,
    end,
):
    length = len(text)
    if navigation_action == "GO":
        handle_move(direction, before_or_after, start, end, length)
    elif navigation_action == "SELECT":
        handle_select(
            navigation_target_name, before_or_after, direction, text, start, end, length
        )
    elif navigation_action == "DELETE":
        handle_select(
            navigation_target_name, before_or_after, direction, text, start, end, length
        )
        actions.edit.delete()
    elif navigation_action == "CUT":
        handle_select(
            navigation_target_name, before_or_after, direction, text, start, end, length
        )
        actions.edit.cut()
    elif navigation_action == "COPY":
        handle_select(
            navigation_target_name, before_or_after, direction, text, start, end, length
        )
        actions.edit.copy()
    elif navigation_action == "EXTEND":
        handle_extend(before_or_after, direction, start, end, length)


def handle_select(
    navigation_target_name, before_or_after, direction, text, start, end, length
):
    if before_or_after == "BEFORE":
        select_left = length - start
        text_left = text[:-select_left]
        match2 = match_backwards(navigation_target_name, 1, text_left)
        if match2 is None:
            end = start
            start = 0
        else:
            start = match2.start()
            end = match2.end()
    elif before_or_after == "AFTER":
        text_right = text[end:]
        match2 = match_forward(navigation_target_name, 1, text_right)
        if match2 is None:
            start = end
            end = length
        else:
            start = end + match2.start()
            end = end + match2.end()
    select(direction, start, end, length)


def handle_move(direction, before_or_after, start, end, length):
    if direction == "RIGHT" or direction == "DOWN":
        if before_or_after == "BEFORE":
            go_right(start)
        else:
            go_right(end)
    else:
        if before_or_after == "AFTER":
            go_left(length - end)
        else:
            go_left(length - start)


def handle_extend(before_or_after, direction, start, end, length):
    if direction == "RIGHT" or direction == "DOWN":
        if before_or_after == "BEFORE":
            extend_right(start)
        else:
            extend_right(end)
    else:
        if before_or_after == "AFTER":
            extend_left(length - end)
        else:
            extend_left(length - start)


def match_backwards(regex, occurrence_number, subtext):
    try:
        match = list(regex.finditer(subtext))[-occurrence_number]
        return match
    except IndexError:
        return


def match_forward(regex, occurrence_number, sub_text):
    try:
        match = next(
            itertools.islice(regex.finditer(sub_text), occurrence_number - 1, None)
        )
        return match
    except StopIteration:
        return None
