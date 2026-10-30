import math
import re
from collections import defaultdict
from collections.abc import Iterable
from typing import Any, Optional

from talon import Context, Module, actions, imgui, registry, settings

from ...core.gui.gui import (
    PageScroller,
    Table,
    TextRow,
    compute_table_height,
    create_bold_text,
    create_italic_text,
    open_gui,
    pad_title_for_two_column_rows,
)

mod = Module()
mod.list("help_contexts", desc="list of available contexts")
mod.tag("help_open", "tag for commands that are available only when help is visible")
mod.setting(
    "help_max_contexts_per_page",
    type=int,
    default=20,
    desc="The maximum number of contexts to display per page in help",
)
mod.setting(
    "help_max_command_lines_per_page",
    type=int,
    default=50,
    desc="The maximum number of lines of commands to display per page in help",
)
mod.setting(
    "help_sort_contexts_by_specificity",
    type=bool,
    default=True,
    desc="Sort contexts by specificity before sorting alphabetically. Otherwise, contexts are just sorted alphabetically.",
)

ctx = Context()
# context name -> commands
context_command_map = {}

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

cached_active_contexts = set()

live_update = True
show_enabled_contexts_only = False

selected_list = None
current_list_page = 1

# used for programmatic scrolling with egui
page_scroller: PageScroller | None = None
# this is being used for the egui migrated guis
current_gui = None


def update_title():
    global live_update
    global show_enabled_contexts_only

    if live_update:
        if gui_context_help.showing:
            if selected_context is None:
                refresh_context_command_map(show_enabled_contexts_only)
            else:
                update_active_contexts_cache(registry.last_active_contexts)
        if gui_operators.showing:
            update_operators_text()


@imgui.open(y=0)
def gui_formatters(gui: imgui.GUI):
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


OPERATORS_MAX_COLUMN_LENGTH = 40


def _add_rows_for_operator(table, prefix, operator_name, description):
    postfix = "" if description else "*"
    operator_name_text = f"    {prefix} {operator_name}{postfix}"
    columns = [operator_name_text]
    if description:
        columns.append(description)
        rich_text_functions = None
    else:
        rich_text_functions = (create_italic_text,)
    table.add_row(TextRow(columns, rich_text_functions=rich_text_functions))


def _compute_operator_description(operator):
    # If the operator is implemented as text insertion,
    # display the operator text
    if isinstance(operator, str):
        return operator
    # If a documentation string is available, use that
    if doc_string := getattr(operator, "__doc__", None):
        return doc_string
    # Otherwise display the operator name from list
    return ""


def _add_rows_for_operator_category_header(table, name):
    row_text = f"{name} operators:"
    table.add_row(TextRow((row_text,), rich_text_functions=(create_bold_text,)))


def _add_missing_text_implementation_footnote(table):
    row_text = "* operator is implemented as a function call and cannot be displayed"
    table.add_row(TextRow((row_text,), rich_text_functions=(create_bold_text,)))


def _compute_operator_list_names_with_prefixes():
    # Associate the names of the operator lists with the corresponding prefix
    op_list_names = ["array", "assignment", "lambda", "math", "pointer"]
    names_with_prefix = [(name, "op") for name in op_list_names]
    names_with_prefix += [("math_comparison", "is"), ("bitwise", "(bit | bitwise)")]
    names_with_prefix.sort()
    return names_with_prefix


def update_operators_text():
    """For operators implemented for the active language, map spoken forms including operator prefix to
    the operator text for operators implemented as text insertion
    or an asterisk for operators implemented as a function call.
    """
    global operators_text
    try:
        operators = actions.user.code_get_operators()
        names_with_prefix = _compute_operator_list_names_with_prefixes()

        # Fill in the table by iterating over the operator lists
        table = Table(OPERATORS_MAX_COLUMN_LENGTH)
        has_operator_without_text_implementation = False
        for name, prefix in names_with_prefix:
            operators_list = actions.user.talon_get_active_registry_list(
                "user.code_operators_" + name
            )
            has_added_first_list_item = False
            for operator_name, operator_text in sorted(operators_list.items()):
                # Only display operators implemented for the active language
                if operator_text in operators:
                    # Only add the header if an item in the list is defined in operators
                    if not has_added_first_list_item:
                        _add_rows_for_operator_category_header(table, name)
                        has_added_first_list_item = True
                    operator = operators.get(operator_text)
                    description = _compute_operator_description(operator)
                    _add_rows_for_operator(table, prefix, operator_name, description)
                    if not description:
                        has_operator_without_text_implementation = True

        if has_operator_without_text_implementation:
            _add_missing_text_implementation_footnote(table)
        page_scroller.page_size = settings.get("user.help_max_command_lines_per_page")
        operators_text = table
    # This exception will get raised if there is no operators object defined in the active context
    except NotImplementedError:
        operators_text = None


def add_help_close_button(ui_wrapper):
    if ui_wrapper.button("Help close"):
        actions.user.help_hide()


def add_page_navigation_buttons(ui_wrapper, scroller):
    if not scroller:
        return

    if ui_wrapper.button("Help next"):
        scroller.page_down()

    if ui_wrapper.button("Help previous"):
        scroller.page_up()


@open_gui(y=0, refresh_period="500ms")
async def gui_operators(ui, ui_wrapper):
    global operators_text
    # use horizontal layout to prevent wrapping
    async with ui.horizontal():
        title = "Help: Operators"
        if operators_text:
            # add padding so the auto sizing creates enough width
            title = pad_title_for_two_column_rows(title, OPERATORS_MAX_COLUMN_LENGTH)
        ui_wrapper.header(title)

    if operators_text is None:
        ui.separator()
        ui.label(
            "There is no active programming language when you opened this menu\nor the language does not have operator support."
        )
    else:
        row_size = ui_wrapper.get_label_row_size()
        maximum_height = compute_table_height(
            row_size, ui_wrapper.get_item_spacing(), page_scroller.page_size
        )

        await ui_wrapper.render_table(
            headers=["", ""],
            table=operators_text,
            maximum_height=maximum_height,
            row_height=row_size,
            id_salt="help_operators",
            scroller=page_scroller,
        )

    ui_wrapper.spacing()
    async with ui.horizontal_wrapped():
        add_help_close_button(ui_wrapper)
        if operators_text and len(operators_text) > page_scroller.page_size:
            add_page_navigation_buttons(ui_wrapper, page_scroller)


def format_context_title(context_name: str) -> str:
    global cached_active_contexts
    return "{} [{}]".format(
        context_name,
        (
            "ACTIVE"
            if context_map.get(context_name) in cached_active_contexts
            else "INACTIVE"
        ),
    )


def format_context_button(index: int, context_label: str, context_name: str) -> str:
    global cached_active_contexts
    global show_enabled_contexts_only
    should_show_asterisk: bool = (
        not show_enabled_contexts_only
        and context_map.get(context_name) in cached_active_contexts
    )
    postfix: str = "*" if should_show_asterisk else ""

    return f"help {index}. {context_label}{postfix}"


# translates 1-based index -> actual index in sorted_context_map_keys
def get_context_page(index: int) -> int:
    return math.ceil(index / settings.get("user.help_max_contexts_per_page"))


def get_total_context_pages() -> int:
    return math.ceil(
        len(sorted_display_list) / settings.get("user.help_max_contexts_per_page")
    )


def get_current_context_page_length() -> int:
    start_index = (current_context_page - 1) * settings.get(
        "user.help_max_contexts_per_page"
    )
    return len(
        sorted_display_list[
            start_index : start_index + settings.get("user.help_max_contexts_per_page")
        ]
    )


def get_command_line_count(command: tuple[str, str]) -> int:
    """This should be kept in sync with draw_commands"""
    _, body = command
    lines = len(body.split("\n"))
    if lines == 1:
        return 1
    return lines + 1


def get_pages(item_line_counts: list[int]) -> list[int]:
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
        if line_count + current_page_line_count > settings.get(
            "user.help_max_command_lines_per_page"
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
    global cached_active_contexts
    global total_page_count
    global search_phrase

    # if no selected context, draw the contexts
    if selected_context is None and search_phrase is None:
        total_page_count = get_total_context_pages()

        if not show_enabled_contexts_only:
            gui.text(
                f"Help: All ({current_context_page}/{total_page_count}) (* = active)"
            )
        else:
            gui.text(
                f"Help: Active Contexts Only ({current_context_page}/{total_page_count})"
            )

        gui.line()

        current_item_index = 1
        current_selection_index = 1
        current_group = ""
        for display_name, group, _ in sorted_display_list:
            target_page = get_context_page(current_item_index)
            context_name = display_name_to_context_name_map[display_name]
            if current_context_page == target_page:
                if current_group != group:
                    if current_group:
                        gui.line()
                    gui.text(f"{group}:")
                    current_group = group

                button_name = format_context_button(
                    current_selection_index,
                    display_name,
                    context_name,
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
        for command, page in zip(commands, pages, strict=False)
        if page == selected_context_page
    ]

    draw_commands(gui, filtered_commands)


def draw_search_commands(gui: imgui.GUI):
    global search_phrase
    global total_page_count
    global cached_active_contexts
    global selected_context_page

    title = f"Search: {search_phrase}"
    commands_grouped = get_search_commands(search_phrase)

    sorted_commands_grouped = sorted(
        commands_grouped.items(),
        key=lambda item: context_map[item[0]] not in cached_active_contexts,
    )

    # flatten to individual commands so get_pages applies the limit per-command, not per-context group
    flat_commands = []
    item_line_counts = []
    for context, commands in sorted_commands_grouped:
        for i, command in enumerate(commands):
            flat_commands.append((context, command))
            # add header overhead (title + separator + spacer) once per context group
            item_line_counts.append(
                get_command_line_count(command) + (3 if i == 0 else 0)
            )
    pages = get_pages(item_line_counts)
    total_page_count = max(pages, default=1)

    draw_commands_title(gui, title)

    current_context = None
    for (context, command), page in zip(flat_commands, pages, strict=True):
        if page != selected_context_page:
            continue
        if context != current_context:
            if current_context is not None:
                gui.spacer()
            gui.text(format_context_title(context))
            gui.line()
            current_context = context
        draw_command(gui, command)


def get_search_commands(phrase: str) -> dict[str, tuple[str, str]]:
    global rule_word_map
    tokens = search_phrase.split(" ")

    viable_commands = rule_word_map[tokens[0]]
    for token in tokens[1:]:
        viable_commands &= rule_word_map[token]

    # sets have no stable sort order, unlike dicts
    viable_commands = list(viable_commands)
    viable_commands.sort()

    commands_grouped = defaultdict(list)
    for context, rule in viable_commands:
        command = context_command_map[context][rule]
        commands_grouped[context].append((rule, command))

    return commands_grouped


def draw_commands_title(gui: imgui.GUI, title: str):
    global selected_context_page
    global total_page_count

    gui.text(f"{title} ({selected_context_page}/{total_page_count})")
    gui.line()


def draw_command(gui: imgui.GUI, command: tuple[str, str]):
    key, val = command
    val = val.split("\n")
    if len(val) > 1:
        gui.text(f"{key}:")
        for line in val:
            gui.text(f"    {line}")
    else:
        gui.text(f"{key}: {val[0]}")


def draw_commands(gui: imgui.GUI, commands: Iterable[tuple[str, str]]):
    for command in commands:
        draw_command(gui, command)


def reset():
    global current_context_page
    global sorted_display_list
    global selected_context
    global search_phrase
    global selected_context_page
    global show_enabled_contexts_only
    global display_name_to_context_name_map
    global selected_list
    global operators_text
    global current_list_page
    global page_scroller
    global current_gui

    current_context_page = 1
    sorted_display_list = []
    selected_context = None
    search_phrase = None
    selected_context_page = 1
    show_enabled_contexts_only = False
    display_name_to_context_name_map = {}
    selected_list = None
    operators_text = None
    current_list_page = 1
    page_scroller = None
    current_gui = None


def update_active_contexts_cache(active_contexts):
    # print("update_active_contexts_cache")
    global cached_active_contexts
    cached_active_contexts = active_contexts


def refresh_context_command_map(enabled_only=False):
    """Update information on command contexts
    enabled_only: indicates if only active contexts should be considered"""
    active_contexts = registry.last_active_contexts
    active_context_cache = set()

    local_context_map = {}
    local_display_name_to_context_name_map = {}
    local_context_command_map = {}
    cached_context_names = {}

    for context_name, context in registry.contexts.items():
        splits = context_name.split(".")
        if splits[-1] != "talon" or (enabled_only and context not in active_contexts):
            continue
        current_context_map = {
            str(val.rule.rule): val.script.code
            for command_alias, val in context.commands.items()
            if not enabled_only or command_alias in registry.commands
        }
        if not current_context_map:
            continue
        if context in active_contexts and is_any_context_command_active(context):
            active_context_cache.add(context)

        local_context_command_map[context_name] = current_context_map

        display_name = splits[-2].replace("_", " ")
        update_spoken_forms(cached_context_names, display_name, context_name)

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

    ctx.lists["user.help_contexts"] = cached_context_names
    update_active_contexts_cache(active_context_cache)


def update_spoken_forms(
    context_spoken_forms: dict[str, str], display_name: str, context_name: str
):
    """Compute spoken forms for a display name and then update context_spoken_forms
    to map those spoken forms to the context name"""
    spoken_forms = actions.user.create_spoken_forms(
        display_name,
        generate_subsequences=False,
    )

    for spoken_form in spoken_forms:
        context_spoken_forms[spoken_form] = context_name


def is_any_context_command_active(context) -> bool:
    """Returns if any command in the context is active"""
    return any(command_alias in registry.commands for command_alias in context.commands)


def get_sorted_display_keys(
    context_map: dict[str, Any],
    display_name_to_context_name_map: dict[str, str],
):
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
) -> list[tuple[str, str, int]]:
    def get_group(display_name) -> tuple[str, str, int]:
        try:
            context_name = display_name_to_context_name_map[display_name]
            context = context_map[context_name]
            keys = context._match.keys()
            if any(key for key in keys if key.startswith("app.")):
                return (display_name, "Application-specific", 2)
            if keys:
                return (display_name, "Context-dependent", 1)
            return (display_name, "Global", 0)
        except:
            return (display_name, "", 0)

    grouped_list = [
        get_group(display_name) for display_name in display_name_to_context_name_map
    ]
    return sorted(
        grouped_list,
        key=lambda item: (-item[2], item[0]),
    )


def refresh_rule_word_map(context_command_map):
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
    gui_operators.hide()


MAX_COLUMN_LENGTH_FOR_HELP_LIST = 20
LIST_KEY_HEADER = "Spoken Form"
LIST_VALUE_HEADER = "Value"


@open_gui(y=0, refresh_period="500ms")
async def gui_list_help(ui, ui_wrapper):
    global selected_list
    global page_scroller

    # clicking the close button forces a refresh even though we are closing this gui.
    # #If we are closing this list, just return
    if not selected_list:
        return

    # show list name and description for the title
    title = f"List: {selected_list}"
    # use the title to claim enough width: add enough padding to show columns with the maximum length
    title = pad_title_for_two_column_rows(title, MAX_COLUMN_LENGTH_FOR_HELP_LIST)

    # Extract description from list declaration, i.e. mod.list(..., desc=...))
    if (desc := registry.decls.lists[selected_list].desc) is not None:
        subtitle = desc
    else:
        subtitle = ""

    ui_wrapper.title(title, subtitle)

    # setup paging handling
    page_size = settings.get("user.help_max_command_lines_per_page")
    page_scroller.page_size = page_size
    row_size = ui_wrapper.get_label_row_size()
    maximum_height = compute_table_height(
        row_size, ui_wrapper.get_item_spacing(), page_size
    )

    # get the list
    talon_list = actions.user.talon_get_active_registry_list(selected_list)
    table = Table(MAX_COLUMN_LENGTH_FOR_HELP_LIST)
    table.add_text_rows(list(talon_list.items()))

    # show the rows in a table
    if table.has_rows():
        headers = [LIST_KEY_HEADER, LIST_VALUE_HEADER]
        await ui_wrapper.render_table(
            headers,
            table,
            maximum_height=maximum_height,
            row_height=row_size,
            id_salt="help_list",
            scroller=page_scroller,
        )

    ui_wrapper.spacing()

    # show navigation buttons. these are arranged horizontally but will wrap onto more rows if needed
    async with ui.horizontal_wrapped():
        add_help_close_button(ui_wrapper)
        if len(table) > page_size:
            add_page_navigation_buttons(ui_wrapper, page_scroller)


@mod.action_class
class Actions:
    def help_list(ab: str):
        """Provides the symbol dictionary"""
        # what you say is stored as a trigger
        global selected_list, current_gui, page_scroller
        hide_all_help_guis()
        reset()
        current_gui = gui_list_help
        selected_list = ab
        page_scroller = PageScroller()
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

    def help_operators():
        """Displays the list of operator names"""
        global page_scroller, current_gui
        reset()
        hide_all_help_guis()
        current_gui = gui_operators
        page_scroller = PageScroller()
        update_operators_text()
        gui_operators.show()
        register_events(True)
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

    def help_search(phrase: str, enabled_only: Optional[bool] = False):
        """Display command info for search phrase"""
        global search_phrase

        reset()
        search_phrase = phrase
        refresh_context_command_map(enabled_only=enabled_only)
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
            update_active_contexts_cache(registry.last_active_contexts)

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

        if page_scroller:
            page_scroller.page_down()
            refresh_gui()
            return

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

    def help_select_index(index: int):
        """Select the context by a number"""
        global sorted_display_list, selected_context
        if gui_context_help.showing:  # noqa: SIM102
            if index < settings.get("user.help_max_contexts_per_page") and (  # noqa: SIM102
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

        if page_scroller:
            page_scroller.page_up()
            refresh_gui()
            return

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
                update_active_contexts_cache(registry.last_active_contexts)

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


def commands_updated(_):
    update_title()


def refresh_gui():
    # egui UIs must be refreshed to update without user interaction
    if current_gui:
        current_gui.refresh()
