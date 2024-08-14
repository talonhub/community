import math
import re
from collections import defaultdict
from functools import cmp_to_key
from itertools import islice
from typing import Any, Iterable, Tuple

from talon import Context, Module, actions, imgui, registry, settings

mod = Module()
mod.list("help_contexts", desc="list of available contexts")
mod.tag("help_open", "tag for commands that are available only when help is visible")
mod.setting(
    "help_max_contexts_per_page",
    type=int,
    default=20,
    desc="Max contexts to display per page in help",
)
mod.setting(
    "help_max_command_lines_per_page",
    type=int,
    default=50,
    desc="Max lines of command to display per page in help",
)
mod.setting(
    "help_sort_contexts_by_specificity",
    type=bool,
    default=True,
    desc="If true contexts are sorted by specificity before alphabetically. If false, contexts are just sorted alphabetically.",
)

ctx = Context()
# context name -> commands
context_command_map: dict[str, dict[str, str]] = {}

# rule word -> Set[(context name, rule)]
rule_word_map: dict[str, set[tuple[str, str]]] = defaultdict(set)
search_phrase = None

# context name -> actual context
context_map = {}

current_context_page = 1
# sorted list of diplay names
sorted_display_list = []
# display names -> context name
display_name_to_context_name_map = {}
selected_context = None
selected_context_page = 1

total_page_count = 1

cached_active_contexts_list = []

live_update = True
show_enabled_contexts_only = False

selected_list = None
current_list_page = 1


def update_title():
    """After commands changed, update the GUI"""
    global live_update
    global show_enabled_contexts_only

    if live_update:
        if gui_context_help.showing:
            if selected_context is None:
                refresh_context_command_map(show_enabled_contexts_only)
            else:
                update_active_contexts_cache(registry.active_contexts())


def commands_updated(_):
    """React to a change in available commands"""
    update_title()


@imgui.open(y=0)
def gui_formatters(gui: imgui.GUI):
    """GUI for formatters with formatter names and example outputs"""
    global formatters_words
    if formatters_reformat:
        gui.text("re-formatters help")
    else:
        gui.text("formatters help")
    gui.line()

    for key, val in formatters_words.items():
        gui.text(f"{val}: {key}")

    gui.spacer()
    gui.text("* prose formatter")
    gui.spacer()
    if gui.button("Help close"):
        gui_formatters.hide()


def format_context_title(context_name: str) -> str:
    """Turn a context name into text to show in the interface.

    Will put "ACTIVE" or "INACTIVE" in brackets after the name depending
    on the current state."""
    global cached_active_contexts_list
    return "{} [{}]".format(
        context_name,
        (
            "ACTIVE"
            if context_map.get(context_name, None) in cached_active_contexts_list
            else "INACTIVE"
        ),
    )


def format_context_button(index: int, context_label: str, context_name: str) -> str:
    """Given an index, label for the context, and its actual name, give text for a button.

    If active and inactive contexts are showing, active contexts get a little * in front.

    The index is put at the front so the user can address it with spoken commands.
    """
    global cached_active_contexts_list
    global show_enabled_contexts_only

    if not show_enabled_contexts_only:
        return "{}. {}{}".format(
            index,
            context_label,
            (
                "*"
                if context_map.get(context_name, None) in cached_active_contexts_list
                else ""
            ),
        )
    else:
        return f"{index}. {context_label} "


def get_context_page(index: int) -> int:
    """translates 1-based index -> actual index in sorted_context_map_keys"""
    return math.ceil(index / settings.get("user.help_max_contexts_per_page"))


def get_total_context_pages() -> int:
    """Get the total number of pages of contexts"""
    return math.ceil(
        len(sorted_display_list) / settings.get("user.help_max_contexts_per_page")
    )


def get_current_context_page_length() -> int:
    """Get the number of entries for the currently shown page"""
    start_index = (current_context_page - 1) * settings.get(
        "user.help_max_contexts_per_page"
    )
    return len(
        sorted_display_list[
            start_index : start_index + settings.get("user.help_max_contexts_per_page")
        ]
    )


def get_command_line_count(command: tuple[str, str]) -> int:
    r"""Output how many lines a command will be printed as.

    Single-line commands are printed on one line, anything longer
    will have an empty line after it.

    >>> get_command_line_count(("florble", "user.florble_thing()"))
    1
    >>> get_command_line_count(("turgle", "\"turgle turgle\"\nkey(enter)\n\"who turgled?\""))
    3
    """
    # This should be kept in sync with draw_commands
    _, body = command
    lines = len(body.split("\n"))
    if lines == 1:
        return 1
    else:
        return lines + 1


def get_pages(item_line_counts: list[int]) -> list[int]:
    """Given some set of indivisible items with given line counts,
    return the page number (1-based) each item should appear on.

    If an item will cross a page boundary, it is moved to the next page,
    so that pages may be shorter than the maximum lenth, but not longer. The only
    exception is when an item is longer than the maximum page length, in which
    case that item will be placed on a longer page.
    """
    current_page_line_count = 0
    current_page = 1
    pages = []
    for line_count in item_line_counts:
        # Will the next entry take us over the limit?
        if line_count + current_page_line_count > settings.get(
            "user.help_max_command_lines_per_page"
        ):
            if current_page_line_count == 0:
                # This is the only item for the page, so it gets
                # a page completely for itself, no matter how big.
                page = current_page
                current_page_line_count = 0
            else:
                # Put the item as the first item on the next page
                page = current_page + 1
                current_page_line_count = line_count
            # In any case, we up the current page by one
            current_page += 1
        else:
            # Count the added lines for the current page
            current_page_line_count += line_count
            page = current_page
        # Store the page the item will appear on into the list
        pages.append(page)
    return pages


@imgui.open(y=0)
def gui_context_help(gui: imgui.GUI):
    """GUI Window for help. Handles context list as well as context content"""
    global context_command_map
    global current_context_page
    global selected_context
    global selected_context_page
    global sorted_display_list
    global show_enabled_contexts_only
    global cached_active_contexts_list
    global total_page_count
    global search_phrase

    # if no selected context, and not showing search results, draw the context list
    if selected_context is None and search_phrase is None:
        total_page_count = get_total_context_pages()

        if not show_enabled_contexts_only:
            gui.text(
                f"Help: All ({current_context_page}/{total_page_count}) (* = active)"
            )
        else:
            gui.text(
                "Help: Active Contexts Only ({}/{})".format(
                    current_context_page, total_page_count
                )
            )

        gui.line()

        # index counting only visible items
        current_entry_index = 1
        current_group = ""
        for current_item_index, (display_name, group, _) in enumerate(
            sorted_display_list, start=1
        ):
            target_page = get_context_page(current_item_index)
            context_name = display_name_to_context_name_map[display_name]
            if current_context_page == target_page:
                # If the group has changed (or is the group of
                # the very first element) show a line and the group title
                if current_group != group:
                    if current_group:
                        gui.line()
                    gui.text(f"{group}:")
                    current_group = group

                button_name = format_context_button(
                    current_entry_index,
                    display_name,
                    context_name,
                )

                if gui.button(button_name):
                    selected_context = context_name
                current_entry_index = current_entry_index + 1

        if total_page_count > 1:
            gui.spacer()
            if gui.button("Help next"):
                actions.user.help_next()

            if gui.button("Help previous"):
                actions.user.help_previous()

    # if there's a selected context, or search results, draw the commands for it
    else:
        if selected_context is not None:
            draw_context_commands(gui)
        elif search_phrase is not None:
            draw_search_commands(gui)

        gui.spacer()
        if total_page_count > 1:
            if gui.button("Help next"):
                actions.user.help_next()

            if gui.button("Help previous"):
                actions.user.help_previous()

        if gui.button("Help return"):
            actions.user.help_return()

    if gui.button("Help refresh"):
        actions.user.help_refresh()

    if gui.button("Help close"):
        actions.user.help_hide()


def draw_context_commands(gui: imgui.GUI):
    """Draw a pageful of commands for the currently selected context.

    Includes a title with page numbers at the top."""
    global selected_context
    global total_page_count
    global selected_context_page

    context_title = format_context_title(selected_context)
    title = f"Context: {context_title}"
    commands = context_command_map[selected_context].items()
    item_line_counts = [get_command_line_count(command) for command in commands]
    pages = get_pages(item_line_counts)
    total_page_count = max(pages, default=1)
    draw_commands_title(gui, title)

    filtered_commands = [
        command
        for command, page in zip(commands, pages)
        if page == selected_context_page
    ]

    draw_commands(gui, filtered_commands)


def draw_search_commands(gui: imgui.GUI):
    """Draw a pageful of search results with title and grouped by context."""
    global search_phrase
    global total_page_count
    global cached_active_contexts_list
    global selected_context_page

    title = f"Search: {search_phrase}"
    commands_grouped = get_search_commands()

    # Bring active contexts to the top of the results
    sorted_commands_grouped = sorted(
        commands_grouped.items(),
        key=lambda item: context_map[item[0]] not in cached_active_contexts_list,
    )

    # Count all lines from one context plus space for title and spacer
    line_counts_of_contexts = [
        sum(get_command_line_count(command) for command in commands) + 3
        for _, commands in sorted_commands_grouped
    ]

    pages = get_pages(line_counts_of_contexts)
    total_page_count = max(pages, default=1)

    draw_commands_title(gui, title)

    for (context, commands), page in zip(sorted_commands_grouped, pages):
        if page == selected_context_page:
            gui.text(format_context_title(context))
            gui.line()
            draw_commands(gui, commands)
            gui.spacer()


def get_search_commands() -> dict[str, list[tuple[str, str]]]:
    """Using the search_phrase, search for commands."""
    global rule_word_map
    tokens = search_phrase.split(" ")

    viable_commands = rule_word_map[tokens[0]]
    for token in tokens[1:]:
        viable_commands &= rule_word_map[token]

    commands_grouped = defaultdict(list)
    for context, rule in viable_commands:
        command = context_command_map[context][rule]
        commands_grouped[context].append((rule, command))

    return commands_grouped


def draw_commands_title(gui: imgui.GUI, title: str):
    """Draw a page's title, page number / total pages, and a horizontal line."""
    global selected_context_page
    global total_page_count

    gui.text(f"{title} ({selected_context_page}/{total_page_count})")
    gui.line()


def draw_commands(gui: imgui.GUI, commands: Iterable[tuple[str, str]]):
    """Draw a list of command / body pairs.

    When the body of the command is just a single line, the command is put in
    front of the body. If the body is more than one line, the command goes on
    its own line up top, and the body is shown below with an indent."""
    for key, val in commands:
        val = val.split("\n")
        if len(val) > 1:
            gui.text(f"{key}:")
            for line in val:
                gui.text(f"    {line}")
        else:
            gui.text(f"{key}: {val[0]}")


def reset():
    global current_context_page
    global sorted_display_list
    global selected_context
    global search_phrase
    global selected_context_page
    global show_enabled_contexts_only
    global display_name_to_context_name_map
    global selected_list
    global current_list_page

    current_context_page = 1
    sorted_display_list = []
    selected_context = None
    search_phrase = None
    selected_context_page = 1
    show_enabled_contexts_only = False
    display_name_to_context_name_map = {}
    selected_list = None
    current_list_page = 1


def update_active_contexts_cache(active_contexts):
    # print("update_active_contexts_cache")
    global cached_active_contexts_list
    cached_active_contexts_list = active_contexts


# example usage todo: make a list definable in .talon
# overrides = {"generic browser": "broswer"}
overrides = {}


def refresh_context_command_map(enabled_only=False):
    """Go through all contexts and collect commands.

    When enabled_only is True, inactive contexts are left out."""
    active_contexts = registry.active_contexts()

    local_context_map = {}
    local_display_name_to_context_name_map = {}
    local_context_command_map = {}
    cached_short_context_names = {}

    for context_name, context in registry.contexts.items():
        splits = context_name.split(".")

        if "talon" == splits[-1]:
            display_name = splits[-2].replace("_", " ")

            short_names = actions.user.create_spoken_forms(
                display_name,
                generate_subsequences=False,
            )

            if short_names[0] in overrides:
                short_names = [overrides[short_names[0]]]
            elif len(short_names) == 2 and short_names[1] in overrides:
                short_names = [overrides[short_names[1]]]

            if enabled_only and context in active_contexts or not enabled_only:
                local_context_command_map[context_name] = {}
                for command_alias, val in context.commands.items():
                    if command_alias in registry.commands or not enabled_only:
                        local_context_command_map[context_name][
                            str(val.rule.rule)
                        ] = val.target.code
                if len(local_context_command_map[context_name]) == 0:
                    local_context_command_map.pop(context_name)
                else:
                    for short_name in short_names:
                        cached_short_context_names[short_name] = context_name

                    # the last entry will contain no symbols
                    local_display_name_to_context_name_map[display_name] = context_name
                    local_context_map[context_name] = context

    # Update all the global state after we've performed our calculations
    global context_map
    global context_command_map
    global sorted_display_list
    global show_enabled_contexts_only
    global display_name_to_context_name_map
    global rule_word_map

    context_map = local_context_map
    context_command_map = local_context_command_map
    sorted_display_list = get_sorted_display_keys(
        local_context_map,
        local_display_name_to_context_name_map,
    )
    show_enabled_contexts_only = enabled_only
    display_name_to_context_name_map = local_display_name_to_context_name_map
    rule_word_map = refresh_rule_word_map(local_context_command_map)

    ctx.lists["self.help_contexts"] = cached_short_context_names
    update_active_contexts_cache(active_contexts)


def get_sorted_display_keys(
    context_map: dict[str, Any],
    display_name_to_context_name_map: dict[str, str],
):
    """Return context names sorted by name, optionally grouped by specificity."""
    if settings.get("user.help_sort_contexts_by_specificity"):
        return get_sorted_keys_by_context_specificity(
            context_map,
            display_name_to_context_name_map,
        )
    return [
        (display_name, "", 0)
        for display_name in sorted(display_name_to_context_name_map.keys())
    ]


def get_sorted_keys_by_context_specificity(
    context_map: dict[str, Any],
    display_name_to_context_name_map: dict[str, str],
) -> list[Tuple[str, str, int]]:
    def get_group(display_name) -> Tuple[str, str, int]:
        try:
            context_name = display_name_to_context_name_map[display_name]
            context = context_map[context_name]
            keys = context._match.keys()
            if any(key for key in keys if key.startswith("app.")):
                return (display_name, "Application-specific", 2)
            if keys:
                return (display_name, "Context-dependent", 1)
            return (display_name, "Global", 0)
        except Exception as ex:
            return (display_name, "", 0)

    grouped_list = [
        get_group(display_name)
        for display_name in display_name_to_context_name_map.keys()
    ]
    return sorted(
        grouped_list,
        key=lambda item: (-item[2], item[0]),
    )


def refresh_rule_word_map(
    context_command_map: dict[str, dict[tuple[str, str]]]
) -> dict[str, set[tuple[str, str]]]:
    """Create a map of word to context/rule that contain it.

    >>> refresh_rule_word_map({
    ...     "one": {"search example": "...", "result": "..."},
    ...     "two": {"search tea": "..."}
    ... })
    {"search": {("one", "search example"), ("two", "search tea")},
     "example": {("one", "search example")},
     "result": {("one", "result")},
     "tea": {("two", "search tea")}}
    """
    rule_word_map = defaultdict(set)

    for context_name, commands in context_command_map.items():
        for rule in commands:
            tokens = {token for token in re.split(r"\W+", rule) if token.isalpha()}
            for token in tokens:
                rule_word_map[token].add((context_name, rule))

    return rule_word_map


events_registered = False


def register_events(register: bool):
    global events_registered
    if register:
        if not events_registered and live_update:
            events_registered = True
            # registry.register('post:update_contexts', contexts_updated)
            registry.register("update_commands", commands_updated)
    else:
        events_registered = False
        # registry.unregister('post:update_contexts', contexts_updated)
        registry.unregister("update_commands", commands_updated)


def hide_all_help_guis():
    gui_context_help.hide()
    gui_formatters.hide()
    gui_list_help.hide()


def paginate_list(data: dict[str, str], SIZE=None):
    chunk_size: int = SIZE or settings.get("user.help_max_command_lines_per_page")
    it = iter(data)
    for _ in range(0, len(data), chunk_size):
        yield {k: data[k] for k in islice(it, chunk_size)}


def make_talonlist_pages():
    """Turn the currently selected list into pages."""
    global selected_list
    global total_page_count

    # FIXME: ListTypeFull can be multiple things, we only support dict[str,str] here
    talon_list = registry.lists[selected_list][-1]

    pages_list = list(paginate_list(talon_list))

    total_page_count = len(pages_list)
    return pages_list


@imgui.open(y=0)
def gui_list_help(gui: imgui.GUI):
    global total_page_count
    global current_list_page
    global selected_list

    pages_list = make_talonlist_pages()

    gui.text(f"{selected_list} {current_list_page}/{total_page_count}")
    gui.line()

    for key, value in pages_list[current_list_page - 1].items():
        gui.text(f"{value}: {key}")

    gui.spacer()

    if total_page_count > 1:
        if gui.button("Help next"):
            actions.user.help_next()

        if gui.button("Help previous"):
            actions.user.help_previous()

    # TODO: until there is a "list of lists", nothing to return to
    # if gui.button("Help return"):
    #    actions.user.help_return()

    # TODO: "help refresh" does nothing when the lists help window is showing
    # if gui.button("Help refresh"):
    #    actions.user.help_refresh()

    if gui.button("Help close"):
        actions.user.help_hide()


@mod.action_class
class Actions:
    def help_list(ab: str):
        """Provides the symbol dictionary"""
        # what you say is stored as a trigger
        global selected_list
        reset()
        selected_list = ab
        gui_list_help.show()
        register_events(True)
        ctx.tags = ["user.help_open"]

    def help_formatters(ab: dict, reformat: bool):
        """Provides the list of formatter keywords"""
        # what you say is stored as a trigger
        global formatters_words, formatters_reformat
        formatters_words = ab
        formatters_reformat = reformat
        reset()
        hide_all_help_guis()
        gui_formatters.show()
        register_events(False)
        ctx.tags = ["user.help_open"]

    def help_context_enabled():
        """Display contextual command info"""
        reset()
        refresh_context_command_map(enabled_only=True)
        hide_all_help_guis()
        gui_context_help.show()
        register_events(True)
        ctx.tags = ["user.help_open"]

    def help_context():
        """Display contextual command info"""
        reset()
        refresh_context_command_map()
        hide_all_help_guis()
        gui_context_help.show()
        register_events(True)
        ctx.tags = ["user.help_open"]

    def help_search(phrase: str):
        """Display command info for search phrase"""
        global search_phrase

        reset()
        search_phrase = phrase
        refresh_context_command_map()
        hide_all_help_guis()
        gui_context_help.show()
        register_events(True)
        ctx.tags = ["user.help_open"]

    def help_selected_context(m: str):
        """Display command info for selected context"""
        global selected_context
        global selected_context_page

        if not gui_context_help.showing:
            reset()
            refresh_context_command_map()
        else:
            selected_context_page = 1
            update_active_contexts_cache(registry.active_contexts())

        selected_context = m
        hide_all_help_guis()
        gui_context_help.show()
        register_events(True)
        ctx.tags = ["user.help_open"]

    def help_next():
        """Navigates to next page"""
        global current_context_page
        global selected_context
        global selected_context_page
        global total_page_count

        global current_list_page

        if gui_context_help.showing:
            if selected_context is None and search_phrase is None:
                if current_context_page != total_page_count:
                    current_context_page += 1
                else:
                    current_context_page = 1
            else:
                if selected_context_page != total_page_count:
                    selected_context_page += 1
                else:
                    selected_context_page = 1

        if gui_list_help.showing:
            if current_list_page != total_page_count:
                current_list_page += 1
            else:
                current_list_page = 1

    def help_select_index(index: int):
        """Select the context by a number"""
        global sorted_display_list, selected_context
        if gui_context_help.showing:
            if index < settings.get("user.help_max_contexts_per_page") and (
                (current_context_page - 1)
                * settings.get("user.help_max_contexts_per_page")
                + index
                < len(sorted_display_list)
            ):
                if selected_context is None:
                    selected_context = display_name_to_context_name_map[
                        sorted_display_list[
                            (current_context_page - 1)
                            * settings.get("user.help_max_contexts_per_page")
                            + index
                        ][0]
                    ]

    def help_previous():
        """Navigates to previous page"""
        global current_context_page
        global selected_context
        global selected_context_page
        global total_page_count

        global current_list_page

        if gui_context_help.showing:
            if selected_context is None and search_phrase is None:
                if current_context_page != 1:
                    current_context_page -= 1
                else:
                    current_context_page = total_page_count

            else:
                if selected_context_page != 1:
                    selected_context_page -= 1
                else:
                    selected_context_page = total_page_count

        if gui_list_help.showing:
            if current_list_page != total_page_count:
                current_list_page -= 1
            else:
                current_list_page = 1

    def help_return():
        """Returns to the main help window"""
        global selected_context
        global selected_context_page
        global show_enabled_contexts_only

        if gui_context_help.showing:
            refresh_context_command_map(show_enabled_contexts_only)
            selected_context_page = 1
            selected_context = None

    def help_refresh():
        """Refreshes the help"""
        global show_enabled_contexts_only
        global selected_context

        if gui_context_help.showing:
            if selected_context is None:
                refresh_context_command_map(show_enabled_contexts_only)
            else:
                update_active_contexts_cache(registry.active_contexts())

    def help_hide():
        """Hides the help"""
        reset()

        # print("help_hide - alphabet gui_alphabet: {}".format(gui_alphabet.showing))
        # print(
        #     "help_hide - gui_context_help showing: {}".format(gui_context_help.showing)
        # )

        hide_all_help_guis()
        refresh_context_command_map()
        register_events(False)
        ctx.tags = []
