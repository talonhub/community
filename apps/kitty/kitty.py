import enum
import json
from collections import ChainMap
from dataclasses import astuple
from functools import partial
from typing import Iterable, Sequence

from talon import Context, Module, actions, app, settings, ui

from ._utils import (
    KITTY_CONF,
    CmdMap,
    UserCmdMap,
    _sock_memo,
    parse_map_cmds,
    run_kitten_client,
)

"""
Kitty is a terminal emulator for Unix systems (including WSL, unofficially).
Learn more at https://sw.kovidgoyal.net.

When this module loads, it will attempt to read your kitty.conf to get your
`listen_on` and `map` directives. Any `map`s found will override the default
key presses used if RCP is not enabled. There are some limitations: kitty commands
that take arguments will not override successfully due to how they are parsed, eg.
`goto_tab -1` will be named "goto_tab_-1", but the Talon action function will
only call `goto_tab` (the `-1` gets passed as an argument when RPC is enabled,
but without RPC we can only refer to the member by name, and `goto_tab` is not
`goto_tab_-1`).

This limitation could be fixed by special-casing such directives. There are 33
that have default key maps and at least a couple dozen more that don't.
"""

mod = Module()
mod.setting(
    "kitty_terminal_mod",
    type=str,
    default="ctrl-shift",
    desc="Should match `kitty_mod` in your kitty.conf.",
)
mod.setting(
    "kitty_use_rpc",
    type=bool,
    default=True,
    desc=(
        "Whether Talon should try to use the `kitten` RPC client for kitty."
        " If this is True and `kitty_rpc_socket` is not set, your kitty.conf"
        " will be scanned for the `listen_on` directive and its value will be"
        " used. If it's False or both `kitty_rpc_socket` and `listen_on` are"
        " unset, fall back to using key presses."
    ),
)
mod.setting(
    "kitty_rpc_socket",
    type=str,
    default="",
    desc=(
        "Should match the `listen_on` directive in your kitty.conf or"
        " `--listen-on` command line option. (When using the CLI option,"
        " you should also set `user.kitty_rpc_socket_verbatim = True`.)"
        " If you have '{kitty_pid}' in the socket name in kitty.conf, be sure"
        " to escape the braces in your Talon config, like: '{{kitty_pid}}'."
    ),
)
mod.setting(
    "kitty_rpc_socket_verbatim",
    type=bool,
    default=False,
    desc=(
        "If True, will not attempt to format the socket name with the active"
        " kitty PID. This is useful if you launch kitty with the command line"
        " options `--one --listen-on`. If you instead use the `listen_on` config"
        " directive in kitty.conf, leave this on False. N.B. that you will most"
        " likely run into problems if you use `--listen-on` without `--one` and"
        " tend to have multiple kitty OS windows running."
    ),
)
# TODO: Add a setting to pass in an RPC password via file, env, or string
mod.apps.kitty = r"""
app.exe: kitty
app.name: kitty
"""

ctx = Context()
ctx.matches = r"""
app: kitty
"""


class KittyCmdMap(CmdMap):
    """Mapping of kitty's mappable actions to their default key combinations.

    The `send_command` method will first check to see if `user.kitty_rpc_socket`
    is set. If it is, `send_command` will use the `kitten` program (distributed
    with kitty) to send the desired command to kitty via its built-in RPC
    system. This bypasses any custom key mappings in kitty.conf so that
    voice commands work even with a heavily modified kitty configuration, and
    even enables kitty commands that may not be bound at all.

    If the socket is not set, `send_command` will fall back to the known default
    key mapping for the command.

    To add new command maps, provide literal strings **that are not f-strings**
    and can be passed to `str.format` with the single kwarg `kitty_mod`. In
    other words, like this: `"{kitty_mod}-enter"` (note the lack of an `f`!).
    The value of `user.kitty_terminal_mod` will be looked up when `str.format`
    is called, which should be in an action class' method.

    Commands that don't have a default binding may be added with an empty string
    as the member value. These commands will work if the user has configured both
    kitty and Talon to use the RPC socket; if not, a warning will be logged
    (via `print`) and sent to the window manager's notification framework via
    `app.notify`.
    """

    # Commands for windows ("splits," in Talon parlance)
    close_window = "close_window", "{kitty_mod}-w"
    focus_visible_window = "focus_visible_window", "{kitty_mod}-f7"
    goto_layout = "goto_layout", ""
    last_used_layout = "last_used_layout", ""
    launch = "launch", ""
    layout_action = "layout_action", ""
    neighboring_window = "neighboring_window", ""
    new_window = "new_window", "{kitty_mod}-enter"
    new_window_with_cwd = "new_window_with_cwd", ""
    next_window = "next_window", "{kitty_mod}-]"
    nth_window = "nth_window", ""
    previous_window = (
        "previous_window",
        "{kitty_mod}-[",
    )  # ] to make "smart" indent behave
    toggle_layout = "toggle_layout", ""

    # Commands for OS Windows ("windows" in Talon)
    new_os_window = "new_os_window", "{kitty_mod}-n"

    # Commands for tabs
    close_tab = "close_tab", "{kitty_mod}-q"
    goto_tab = "goto_tab", ""
    new_tab = "new_tab", "{kitty_mod}-t"
    new_tab_with_cwd = "new_tab_with_cwd", ""
    next_tab = "next_tab", "{kitty_mod}-right"
    previous_tab = "previous_tab", "{kitty_mod}-left"
    select_tab = "select_tab", ""

    # Commands for copy/paste
    copy_to_clipboard = "copy_to_clipboard", "{kitty_mod}-c"
    paste_from_clipboard = "paste_from_clipboard", "{kitty_mod}-v"
    paste_from_selection = "paste_from_selection", "{kitty_mod}-s"

    # Scrolling
    scroll_line_down = "scroll_line_down", "{kitty_mod}-down"
    scroll_line_up = "scroll_line_up", "{kitty_mod}-up"
    scroll_page_down = "scroll_page_down", "{kitty_mod}-pagedown"
    scroll_page_up = "scroll_page_up", "{kitty_mod}-pageup"

    # Misc
    open_url_with_hints = "open_url_with_hints", "{kitty_mod}-e"
    show_scrollback = "show_scrollback", "{kitty_mod}-h"

    # Mappings specific to the Hints kitten
    # See https://sw.kovidgoyal.net/kitty/kittens/hints/ for details.
    hint_hash = (
        "kitten",
        "{kitty_mod}+p h",
        ("hints", "--type", "hash", "--program", "-"),
    )
    hint_line = (
        "kitten",
        "{kitty_mod}+p l",
        ("hints", "--type", "line", "--program", "-"),
    )
    hint_line_clip = (
        "kitten",
        "{kitty_mod}+p l",
        ("hints", "--type", "line", "--program", "@"),
    )
    hint_line_in_file = "kitten", "{kitty_mod}+p n", ("hints", "--type", "linenum")
    hint_path_clip = (
        "kitten",
        "{kitty_mod}+p f",
        ("hints", "--type", "path", "--program", "@"),
    )
    hint_path_insert = (
        "kitten",
        "{kitty_mod}+p f",
        ("hints", "--type", "path", "--program", "-"),
    )
    hint_path_open = "kitten", "{kitty_mod}+p shift+f", ("hints", "--type", "path")
    hint_word = (
        "kitten",
        "{kitty_mod}+p w",
        ("hints", "--type", "word", "--program", "-"),
    )
    hint_word_clip = (
        "kitten",
        "{kitty_mod}+p w",
        ("hints", "--type", "word", "--program", "@"),
    )
    hint_terminal_link = "kitten", "{kitty_mod}+p y", ("hints", "--type", "hyperlink")


if UserCmdMap is not None:
    cm = ChainMap(
        {m: v for m, v in UserCmdMap.__members__.items()},  # type: ignore
        {m: v for m, v in KittyCmdMap.__members__.items()},
    )
    OverrideCmdMap = CmdMap(
        "OverrideCmdMap",
        {m: astuple(v) for m, v in cm.items()},
    )
    _KittyCmdMap = KittyCmdMap
    KittyCmdMap = OverrideCmdMap  # type: ignore


def _get_active_tab_layout() -> str:
    """Query kitty for the layout of the currently active tab."""
    # Equivalent to:
    #     kitten @ ls | jq 'if (. | type) == "array"
    #         then select(.[].is_focused == true)
    #         end
    #         | .[0].tabs
    #         | select(.[].is_active == true)
    #         | .[0].layout'
    all_kitties = json.loads(
        run_kitten_client(_sock_memo(ui.active_window().app.pid), ["ls"]).stdout
    )
    if isinstance(all_kitties, list):
        active_kitty = next(filter(lambda k: k["is_focused"] == True, all_kitties))
    else:
        active_kitty = all_kitties
    active_tab = next(
        filter(
            lambda t: t["is_active"],
            active_kitty["tabs"],
        )
    )
    return active_tab["layout"]


@ctx.action_class("user")
class UserActions:
    # Implement user.splits
    def split_window():
        KittyCmdMap.new_window.send_command()

    def split_next():
        KittyCmdMap.next_window.send_command()

    def split_last():
        KittyCmdMap.previous_window.send_command()

    def split_number(index: int):
        KittyCmdMap.nth_window.send_command(str(index))

    def split_clear():
        """Close the current window/split."""
        KittyCmdMap.close_window.send_command()

    def split_window_vertically():
        KittyCmdMap.launch.send_command("--location=vsplit")

    def split_window_horizontally():
        KittyCmdMap.launch.send_command("--location=hsplit")

    def split_maximize():
        KittyCmdMap.goto_layout.send_command("stack")

    def split_flip():
        layout = _get_active_tab_layout()
        if layout == "splits":
            KittyCmdMap.layout_action.send_command("rotate")
        elif layout in ("tall", "fat"):
            KittyCmdMap.layout_action.send_command("mirror")

    def split_reset():
        """This only goes to the previously used layout and is most useful for
        reverting "split maximize." It won't equalize split sizes or anything
        cool like that.
        """
        KittyCmdMap.last_used_layout.send_command()

    # Implement a couple tab commands
    def tab_jump(number: int):
        KittyCmdMap.goto_tab.send_command(str(number))

    def tab_duplicate():
        """Opens a new tab in $PWD.

        It does *not* copy the shell environment, scrollback, etc.
        (The `clone-in-kitty` command *can* copy the shell environment, but
        no voice command is bound to it here.)

        N.B. that in ssh sessions created with `kitten ssh`, this command
        will open the new tab _in $PWD on the remote host_.
        """
        KittyCmdMap.new_tab_with_cwd.send_command()


@mod.action_class
class KittyActions:
    """Novel commands just for kitty"""

    # Extra split commands
    def split_window_here():
        """Opens a new kitty window/Talon split in $PWD.

        It does *not* copy the shell environment, scrollback, etc.

        N.B. that in ssh sessions created with `kitten ssh`, this command
        will open the new window _in $PWD on the remote host_.
        """
        KittyCmdMap.new_window_with_cwd.send_command()

    def split_relative(arrow: str):
        """Like `split_number`, but uses relative directions instead of numbers."""
        KittyCmdMap.neighboring_window.send_command(arrow)

    def split_switch():
        """Let "split last" mean "go to the previous split in the list", and
        "split switch" covers the meaning of "go to the split I was in
        previously."
        """
        KittyCmdMap.nth_window.send_command("-1")

    def split_choose():
        """Start kitty's interactive window chooser.

        Each window will get an number overlay. Give the number as you would
        normally "press" a number, i.e. say "num two," to focus that window.
        """
        KittyCmdMap.focus_visible_window.send_command()

    # Extra tab commands
    def tab_choose():
        """Start kitty's interactive tab chooser.

        An enumerated list of tabs will be overlayed on the active window. Say
        the number of the tab you want.
        """
        KittyCmdMap.select_tab.send_command()

    def tab_switch():
        """Let "tab last" mean "go to the previous tab in the list", and
        "tab switch" covers the meaning of "go to the tab I was in
        previously."
        """
        KittyCmdMap.goto_tab.send_command("-1")

    # Misc
    def kitten_insert(kitten: str):
        """Insert `kitten <kitten_name>` into the command line to run kittens
        other than the RPC kitten.

        A list of kittens can be found by running `kitten -h`, using the voice
        command "kitten help," or, for the most info, in the docs at:
        https://sw.kovidgoyal.net/kitty/kittens_intro/

        Stops short of inserting "enter" so you can make sure the kitten you
        intended to run is the one on the command line.
        """
        # As of May 2025, all built-in kitten names are kebab-cased. But, it
        # turns out calling `insert_formatted` on text preformatted with the
        # the given format actually removes the formatting. There are, at time
        # of writing, two cases where we replace the Talon-interpreted text
        # with such strings; rebinding the name of a callable is an easy way to
        # accommodate those and future cases.
        inserter = partial(
            actions.user.insert_formatted,
            formatters="DASH_SEPARATED",
        )
        match kitten:
            case "I cat" | "eye cat":
                kitten = "icat"
            case "S S H":
                kitten = "ssh"
            case "hyperlinked grip":
                kitten = "hyperlinked-grep"
                inserter = actions.insert
            case "at":
                kitten = "@"
            case "help":
                kitten = "--help"
                inserter = actions.insert
            case "di" | "death" | "iff" | "duff" | "tiff":
                kitten = "diff"
        actions.insert("kitten ")
        inserter(kitten)
        actions.key("space")

    def hint_url():
        """Start a hints overlay for opening visible URLs in a browser."""
        KittyCmdMap.open_url_with_hints.send_command()

    def hint_hash():
        """Start a hints overlay for copying visible hashes to the command-line."""
        KittyCmdMap.hint_hash.send_command()

    def hint_line():
        """Start a hints overlay for copying visible lines to the command-line."""
        KittyCmdMap.hint_line.send_command()

    def hint_line_clip():
        """Start a hints overlay for copying visible lines to the clipboard."""
        KittyCmdMap.hint_line_clip.send_command()

    def hint_line_in_file():
        """Start a hints overlay for opening a file to a line with `editor`.

        Eg., `/path/to/file:50` will open the file to line 50.
        """
        KittyCmdMap.hint_line_in_file.send_command()

    def hint_path_clip():
        """Start a hints overlay for copying visible paths to the clipboard."""
        KittyCmdMap.hint_path_clip.send_command()

    def hint_path_insert():
        """Start a hints overlay for copying visible paths to the command-line."""
        KittyCmdMap.hint_path_insert.send_command()

    def hint_path_open():
        """Start a hints overlay for opening visible paths with the program associated
        with the file type."""
        KittyCmdMap.hint_path_open.send_command()

    def hint_word():
        """Start a hints overlay for copying visible words to the command-line."""
        KittyCmdMap.hint_word.send_command()

    def hint_word_clip():
        """Start a hints overlay for copying visible words to the clipboard."""
        KittyCmdMap.hint_word_clip.send_command()

    def hint_terminal_link():
        """Start a hints overlay for opening terminal hyperlinks with a program
        appropriate to the URL scheme, if possible."""
        KittyCmdMap.hint_terminal_link.send_command()


@ctx.action_class("app")
class AppActions:
    # Implement app.tabs
    def tab_open():
        KittyCmdMap.new_tab.send_command()

    def tab_previous():
        KittyCmdMap.previous_tab.send_command()

    def tab_next():
        KittyCmdMap.next_tab.send_command()

    def tab_close():
        KittyCmdMap.close_tab.send_command()

    # global (overwrite linux/app.py)
    def window_open():
        """
        N.B. that your kitty.conf controls whether the new (OS) window is in
        its own process or is owned by the same process as the window that was
        active when this function was called.
        """
        KittyCmdMap.new_os_window.send_command()

    # We don't need to override `window_close`, as alt-F4 will generally do the
    # trick on Linux.


# global (overwrite linux/edit.py)
@ctx.action_class("edit")
class EditActions:
    def page_down():
        KittyCmdMap.scroll_page_down.send_command()

    def page_up():
        KittyCmdMap.scroll_page_up.send_command()

    def paste():
        KittyCmdMap.paste_from_clipboard.send_command()

    def copy():
        KittyCmdMap.copy_to_clipboard.send_command()

    def selection_clone():
        KittyCmdMap.paste_from_selection.send_command()

    # Opens the history kitten and assumes that the pager is `less` to initiate
    # a backwards search for the given text. If no text is given, only open the
    # kitten and pager.
    def find(text: str = ""):
        KittyCmdMap.show_scrollback.send_command()
        if text:
            actions.key("?")
            actions.insert(text)
