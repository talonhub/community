import re
from talon import ctrl, ui, Module, Context, actions, clip
import itertools
from typing import Union

ctx = Context()
mod = Module()


text_navigation_max_line_search = mod.setting(
    "text_navigation_max_line_search",
    type=int,
    default=10,
    desc="With this you can set the maximum number of rows that will be included in the search for the keywords above and below in <user direction>",
)

mod.list(
    "cursor_location",
    desc="words to indicate if the cursor should be moved before or after a given reference point",
)

mod.list(
    "navigation_option",
    desc="words to indicate type of navigation, for instance moving or selecting",
)
mod.list(
    "search_option",
    desc="words to indicate type of search, for instance matching a word with or without underscores",
)

ctx.lists["self.cursor_location"] = {
    "before": "BEFORE",
    "after": "AFTER",
    # DEFAULT is also a valid option as input for this capture, but is not directly accessible for the user.
}

ctx.lists["self.navigation_option"] = {
    "move": "GO",
    "extend": "EXTEND",
    "select": "SELECT",
    "delete": "DELETE",
    "cut": "CUT",
    "copy": "COPY",
}
search_option_list = {
    "word": r"\w+",
    "small": r"[A-Z]?[a-z0-9]+",
    "big": r"[\S]+",
}
ctx.lists["self.search_option"] = search_option_list


@mod.action_class
class Actions:
    def navigation(
        navigation_option: str,
        direction: str,
        cursor_location: str,
        text: str,
        occurrence_number: int,
    ):
        """navigate in the given direction to the occurrence_number-th time that the input text occurs, then execute the navigation_option at the given cursor_location"""
        actions.user.navigation_regex(
            navigation_option,
            direction,
            cursor_location,
            re.compile(re.escape(text), re.IGNORECASE),
            int(occurrence_number),
        )

    # All other navigation commands dispatch to this one, so if you want to
    # override its behavior, this is the one to override.
    def navigation_regex(
        navigation_option: str,
        direction: str,
        cursor_location: str,
        regex: Union[str, re.Pattern],
        occurrence_number: int,
    ):
        """navigate in the given direction to the occurrence_number-th time that the input regex occurs, then execute the navigation_option at the given cursor_location"""
        navigation(
            navigation_option,
            direction,
            cursor_location,
            regex if isinstance(regex, re.Pattern) else re.compile(regex),
            int(occurrence_number),
        )

    def navigation_search_option(
        navigation_option: str,
        direction: str,
        cursor_location: str,
        search_option: str,
        occurrence_number: int,
    ):
        """navigate in the given direction to the occurrence_number-th time that the input search_option occurs, then execute the navigation_option at the given cursor_location"""
        actions.user.navigation_regex(
            navigation_option,
            direction,
            cursor_location,
            search_option_list[search_option],
            int(occurrence_number),
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
    for j in range(0, text_navigation_max_line_search.get()):
        actions.edit.extend_up()
    actions.edit.extend_line_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text


def get_text_down():
    actions.edit.down()
    actions.edit.line_start()
    for j in range(0, text_navigation_max_line_search.get()):
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


def navigation(navigation_option, direction, cursor_location, regex, occurrence_number):
    direction = direction.upper()
    if direction == "LEFT" or direction == "UP":
        navigate_left(
            navigation_option, cursor_location, regex, occurrence_number, direction,
        )
    else:
        navigate_right(
            navigation_option, cursor_location, regex, occurrence_number, direction,
        )


def navigate_left(
    navigation_option, cursor_location, regex, occurrence_number, direction
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
    if match == None:
        # put back the old selection, if the search failed
        extend_left(current_selection_length)
        return
    start = match.start()
    end = match.end()
    handle_navigation_option(
        navigation_option, cursor_location, direction, text, start, end
    )


def navigate_right(
    navigation_option, cursor_location, regex, occurrence_number, direction
):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0:
        actions.edit.left()
    text = get_text_right() if direction == "RIGHT" else get_text_down()
    # only search in the text that was not selected
    sub_text = text[current_selection_length:]
    # pick the next interrater, Skip n number of occurrences, get an iterator given the Regex
    match = match_forward(regex, occurrence_number, sub_text)
    if match == None:
        # put back the old selection, if the search failed
        extend_right(current_selection_length)
        return
    start = current_selection_length + match.start()
    end = current_selection_length + match.end()
    handle_navigation_option(
        navigation_option, cursor_location, direction, text, start, end
    )


def handle_navigation_option(
    navigation_option, cursor_location, direction, text, start, end
):
    length = len(text)
    if navigation_option == "GO":
        handle_move(direction, cursor_location, start, end, length)
    elif navigation_option == "SELECT":
        handle_select(cursor_location, direction, text, start, end, length)
    elif navigation_option == "DELETE":
        handle_select(cursor_location, direction, text, start, end, length)
        actions.edit.delete()
    elif navigation_option == "CUT":
        handle_select(cursor_location, direction, text, start, end, length)
        actions.edit.cut()
    elif navigation_option == "COPY":
        handle_select(cursor_location, direction, text, start, end, length)
        actions.edit.copy()
    elif navigation_option == "EXTEND":
        handle_extend(cursor_location, direction, start, end, length)


def handle_select(cursor_location, direction, text, start, end, length):
    if cursor_location == "BEFORE":
        select_left = length - start
        text_left = text[:-select_left]
        match2 = match_backwards(re.compile(search_option_list["word"]), 1, text_left)
        if match2 == None:
            end = start
            start = 0
        else:
            start = match2.start()
            end = match2.end()
    elif cursor_location == "AFTER":
        text_right = text[end:]
        match2 = match_forward(re.compile(search_option_list["word"]), 1, text_right)
        if match2 == None:
            start = end
            end = length
        else:
            start = end + match2.start()
            end = end + match2.end()
    select(direction, start, end, length)


def handle_move(direction, cursor_location, start, end, length):
    if direction == "RIGHT" or direction == "DOWN":
        if cursor_location == "BEFORE":
            go_right(start)
        else:
            go_right(end)
    else:
        if cursor_location == "AFTER":
            go_left(length - end)
        else:
            go_left(length - start)


def handle_extend(cursor_location, direction, start, end, length):
    if direction == "RIGHT" or direction == "DOWN":
        if cursor_location == "BEFORE":
            extend_right(start)
        else:
            extend_right(end)
    else:
        if cursor_location == "AFTER":
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
