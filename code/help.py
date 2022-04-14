from collections import defaultdict
import itertools
import math
import re
from typing import Dict, List, Iterable, Set, Tuple, Union

from talon import Module, Context, actions, imgui, Module, registry, ui, app
from talon.grammar import Phrase

from itertools import islice

mod = Module()
mod.list("help_contexts", desc="list of available contexts")
mod.mode("help", "mode for commands that are available only when help is visible")
setting_help_max_contexts_per_page = mod.setting(
    "help_max_contexts_per_page",
    type=int,
    default=20,
    desc="Max contexts to display per page in help",
)
setting_help_max_command_lines_per_page = mod.setting(
    "help_max_command_lines_per_page",
    type=int,
    default=50,
    desc="Max lines of command to display per page in help",
)

ctx = Context()
# context name -> commands
context_command_map = {}

# rule word -> Set[(context name, rule)]
rule_word_map: Dict[str, Set[Tuple[str, str]]] = defaultdict(set)
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
    global live_update
    global show_enabled_contexts_only

    if live_update:
        if gui_context_help.showing:
            if selected_context == None:
                refresh_context_command_map(show_enabled_contexts_only)
            else:
                update_active_contexts_cache(registry.active_contexts())


@imgui.open(y=0)
def gui_formatters(gui: imgui.GUI):
    global formatters_words
    gui.text("formatters help")
    gui.line()

    for key, val in formatters_words.items():
        gui.text("{}: {}".format(val, key))

    gui.spacer()
    if gui.button("Help close"):
        gui_formatters.hide()



def format_context_title(context_name: str) -> str:
    global cached_active_contexts_list
    return "{} [{}]".format(
        context_name,
        "ACTIVE"
        if context_map.get(context_name, None) in cached_active_contexts_list
        else "INACTIVE",
    )


def format_context_button(index: int, context_label: str, context_name: str) -> str:
    global cached_active_contexts_list
    global show_enabled_contexts_only

    if not show_enabled_contexts_only:
        return "{}. {}{}".format(
            index,
            context_label,
            "*"
            if context_map.get(context_name, None) in cached_active_contexts_list
            else "",
        )
    else:
        return "{}. {} ".format(index, context_label)


# translates 1-based index -> actual index in sorted_context_map_keys
def get_context_page(index: int) -> int:
    return math.ceil(index / setting_help_max_contexts_per_page.get())


def get_total_context_pages() -> int:
    return math.ceil(
        len(sorted_display_list) / setting_help_max_contexts_per_page.get()
    )


def get_current_context_page_length() -> int:
    start_index = (current_context_page - 1) * setting_help_max_contexts_per_page.get()
    return len(
        sorted_display_list[
            start_index : start_index + setting_help_max_contexts_per_page.get()
        ]
    )


def get_command_line_count(command: Tuple[str, str]) -> int:
    """This should be kept in sync with draw_commands"""
    _, body = command
    lines = len(body.split("\n"))
    if lines == 1:
        return 1
    else:
        return lines + 1


def get_pages(item_line_counts: List[int]) -> List[int]:
    """Given some set of indivisible items with given line counts,
    return the page number each item should appear on.

    If an item will cross a page boundary, it is moved to the next page,
    so that pages may be shorter than the maximum lenth, but not longer. The only
    exception is when an item is longer than the maximum page length, in which
    case that item will be placed on a longer page.
    """
    current_page_line_count = 0
    current_page = 1
    pages = []
    for line_count in item_line_counts:
        if (
            line_count + current_page_line_count
            > setting_help_max_command_lines_per_page.get()
        ):
            if current_page_line_count == 0:
                # Special case, render a larger page.
                page = current_page
                current_page_line_count = 0
            else:
                page = current_page + 1
                current_page_line_count = line_count
            current_page += 1
        else:
            current_page_line_count += line_count
            page = current_page
        pages.append(page)
    return pages


@imgui.open(y=0)
def gui_context_help(gui: imgui.GUI):
    global context_command_map
    global current_context_page
    global selected_context
    global selected_context_page
    global sorted_display_list
    global show_enabled_contexts_only
    global cached_active_contexts_list
    global total_page_count
    global search_phrase

    # if no selected context, draw the contexts
    if selected_context is None and search_phrase is None:
        total_page_count = get_total_context_pages()

        if not show_enabled_contexts_only:
            gui.text(
                "Help: All ({}/{}) (* = active)".format(
                    current_context_page, total_page_count
                )
            )
        else:
            gui.text(
                "Help: Active Contexts Only ({}/{})".format(
                    current_context_page, total_page_count
                )
            )

        gui.line()

        current_item_index = 1
        current_selection_index = 1
        for display_name in sorted_display_list:
            target_page = get_context_page(current_item_index)
            context_name = display_name_to_context_name_map[display_name]
            if current_context_page == target_page:
                button_name = format_context_button(
                    current_selection_index, display_name, context_name,
                )

                if gui.button(button_name):
                    selected_context = context_name
                current_selection_index = current_selection_index + 1

            current_item_index += 1

        if total_page_count > 1:
            gui.spacer()
            if gui.button("Help next"):
                actions.user.help_next()

            if gui.button("Help previous"):
                actions.user.help_previous()

    # if there's a selected context, draw the commands for it
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
    global search_phrase
    global total_page_count
    global cached_active_contexts_list
    global selected_context_page

    title = f"Search: {search_phrase}"
    commands_grouped = get_search_commands(search_phrase)
    commands_flat = list(itertools.chain.from_iterable(commands_grouped.values()))

    sorted_commands_grouped = sorted(
        commands_grouped.items(),
        key=lambda item: context_map[item[0]] not in cached_active_contexts_list,
    )

    pages = get_pages(
        [
            sum(get_command_line_count(command) for command in commands) + 3
            for _, commands in sorted_commands_grouped
        ]
    )
    total_page_count = max(pages, default=1)

    draw_commands_title(gui, title)

    current_item_index = 1
    for (context, commands), page in zip(sorted_commands_grouped, pages):
        if page == selected_context_page:
            gui.text(format_context_title(context))
            gui.line()
            draw_commands(gui, commands)
            gui.spacer()


def get_search_commands(phrase: str) -> Dict[str, Tuple[str, str]]:
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
    global selected_context_page
    global total_page_count

    gui.text("{} ({}/{})".format(title, selected_context_page, total_page_count))
    gui.line()


def draw_commands(gui: imgui.GUI, commands: Iterable[Tuple[str, str]]):
    for key, val in commands:
        val = val.split("\n")
        if len(val) > 1:
            gui.text("{}:".format(key))
            for line in val:
                gui.text("    {}".format(line))
        else:
            gui.text("{}: {}".format(key, val[0]))


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
                display_name, generate_subsequences=False,
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
    sorted_display_list = sorted(local_display_name_to_context_name_map.keys())
    show_enabled_contexts_only = enabled_only
    display_name_to_context_name_map = local_display_name_to_context_name_map
    rule_word_map = refresh_rule_word_map(local_context_command_map)

    ctx.lists["self.help_contexts"] = cached_short_context_names
    update_active_contexts_cache(active_contexts)


def refresh_rule_word_map(context_command_map):
    rule_word_map = defaultdict(set)

    for context_name, commands in context_command_map.items():
        for rule in commands:
            tokens = set(token for token in re.split(r'\W+', rule) if token.isalpha())
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

def paginate_list(data, SIZE=None):
    chunk_size = SIZE or setting_help_max_command_lines_per_page.get()
    it = iter(data)
    for i in range(0, len(data), chunk_size):
        yield {k:data[k] for k in islice(it, chunk_size)}

def draw_list_commands(gui: imgui.GUI):
    global selected_list
    global total_page_count
    global selected_context_page

    talon_list = registry.lists[selected_list][0]
    #numpages = math.ceil(len(talon_list) / SIZE)

    pages_list = []

    for item in paginate_list(talon_list):
        pages_list.append(item)
    #print(pages_list)

    total_page_count = len(pages_list)
    return pages_list

@imgui.open(y=0)
def gui_list_help(gui: imgui.GUI):
    global total_page_count
    global current_list_page
    global selected_list

    pages_list = draw_list_commands(gui)
    total_page_count = len(pages_list)
    #print(pages_list[current_page])

    gui.text("{} {}/{}".format(selected_list, current_list_page, total_page_count))

    gui.line()

    for key, value in pages_list[current_list_page - 1].items():
        gui.text("{}: {}".format(value, key))

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
        actions.mode.enable("user.help")



    def help_formatters(ab: dict):
        """Provides the list of formatter keywords"""
        # what you say is stored as a trigger
        global formatters_words
        formatters_words = ab
        reset()
        # print("help_alphabet - alphabet gui_alphabet: {}".format(gui_alphabet.showing))
        # print(
        #     "help_alphabet - gui_context_help showing: {}".format(
        #         gui_context_help.showing
        #     )
        # )
        hide_all_help_guis()
        gui_formatters.show()
        register_events(False)
        actions.mode.enable("user.help")



    def help_context_enabled():
        """Display contextual command info"""
        reset()
        refresh_context_command_map(enabled_only=True)
        hide_all_help_guis()
        gui_context_help.show()
        register_events(True)
        actions.mode.enable("user.help")

    def help_context():
        """Display contextual command info"""
        reset()
        refresh_context_command_map()
        hide_all_help_guis()
        gui_context_help.show()
        register_events(True)
        actions.mode.enable("user.help")

    def help_search(phrase: str):
        """Display command info for search phrase"""
        global search_phrase

        reset()
        search_phrase = phrase
        refresh_context_command_map()
        hide_all_help_guis()
        gui_context_help.show()
        register_events(True)
        actions.mode.enable("user.help")

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
        actions.mode.enable("user.help")

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
            if index < setting_help_max_contexts_per_page.get() and (
                (current_context_page - 1) * setting_help_max_contexts_per_page.get()
                + index
                < len(sorted_display_list)
            ):
                if selected_context is None:
                    selected_context = display_name_to_context_name_map[
                        sorted_display_list[
                            (current_context_page - 1)
                            * setting_help_max_contexts_per_page.get()
                            + index
                        ]
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
            if selected_context == None:
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
        actions.mode.disable("user.help")

def commands_updated(_):
    update_title()
