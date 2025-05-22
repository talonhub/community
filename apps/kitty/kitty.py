import enum
import json
import subprocess
from functools import cache
from typing import Iterable

from talon import Context, Module, actions, app, settings, ui

"""
Kitty is a terminal emulator for Unix systems (including WSL, unofficially).
Learn more at https://sw.kovidgoyal.net.

The bindings set here assume that your kitty.conf doesn't deviate too far from
the default keybindings.
"""

mod = Module()
mod.setting(
    "kitty_terminal_mod",
    type=str,
    default="ctrl-shift",
    desc="Should match `kitty_mod` in your kitty.conf.",
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
ctx.tags = [
    "terminal",
    "user.tabs",
    "user.splits",
    "user.readline",
    "user.generic_unix_shell",
    "user.git",
]


def run_kitten_client(sock: str, args: Iterable[str]):
    """Send a "mappable action" to kitty via the built-in `kitten` RPC client.

    A complete list of mappable actions can be found at:
    https://sw.kovidgoyal.net/kitty/actions/

    Essentially, these are any command that might be targetted by a `map`
    directive in kitty.conf.
    """
    return subprocess.run(
        ["kitten", "@", "--to", sock, *args],
        capture_output=True,
        universal_newlines=True,
    )


def KITTY_MOD():
    """Fetch the user's configured `kitty_terminal_mod`, if set.

    Override this in your own settings:
        -
        settings():
            user.kitty_terminal_mod = <combo that matches your kitty.conf>

    This has to be a function to defer fetching the value until it's definitely
    been read by Talon.
    """
    return settings.get("user.kitty_terminal_mod")


@cache
def _sock_memo(active_win_pid: int):
    """Memoize formatted socket paths for each kitty PID."""
    # Possibly a premature optimization: the time to return (measured by
    # ipython's %timeit) was over 4.5x faster vs doing the string formatting
    # every time. Sounds pretty cool... but 4.5 * 35.3ns is still only 160ns.
    sock = settings.get("user.kitty_rpc_socket")
    if sock and not settings.get("user.kitty_rpc_socket_verbatim"):
        if "{kitty_pid}" in sock:
            sock = sock.format(kitty_pid=active_win_pid)
        else:
            sock = sock + f"-{active_win_pid}"
    return sock


# Clear the cache if Talon reloads, just in case kitty_rpc_socket was one of
# the things that changed to trigger the reload.
app.register("ready", _sock_memo.cache_clear)


class KittyCmdMap(enum.Enum):
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
    close_window = "{kitty_mod}-w"
    focus_visible_window = "{kitty_mod}-f7"
    goto_layout = ""
    last_used_layout = ""
    launch = ""
    layout_action = ""
    neighboring_window = ""
    new_window = "{kitty_mod}-enter"
    new_window_with_cwd = ""
    next_window = "{kitty_mod}-]"
    nth_window = ""
    previous_window = "{kitty_mod}-["  # ] to make "smart" indent behave
    toggle_layout = ""

    # Commands for OS Windows ("windows" in Talon)
    new_os_window = "{kitty_mod}-n"

    # Commands for tabs
    close_tab = "{kitty_mod}-q"
    goto_tab = ""
    new_tab = "{kitty_mod}-t"
    new_tab_with_cwd = ""
    next_tab = "{kitty_mod}-right"
    previous_tab = "{kitty_mod}-left"

    # Commands for copy/paste
    copy_to_clipboard = "{kitty_mod}-c"
    paste_from_clipboard = "{kitty_mod}-v"
    paste_from_selection = "{kitty_mod}-s"

    # Scrolling
    scroll_line_down = "{kitty_mod}-down"
    scroll_line_up = "{kitty_mod}-up"
    scroll_page_down = "{kitty_mod}-pagedown"
    scroll_page_up = "{kitty_mod}-pageup"

    # Misc
    show_scrollback = "{kitty_mod}-h"

    def __new__(cls, key_combo):
        member = object.__new__(cls)
        # Allows us to use `""` as the value for multiple members without them
        # being considered duplicates/aliases.
        member._value_ = key_combo or object()
        return member

    @enum.property
    def key_combo(self):
        if isinstance(self._value_, str):
            return self._value_
        return ""

    def send_command(self, *args):
        """Execute the kitty command, using the RPC kitten if possible or the
        default keybinding otherwise.
        """
        # TODO: Versions of kitty newer than what Ubuntu packages as of May 2025
        # have a third option where a new OS window can be launched but hidden
        # and attached to the active kitty process, meaning the `kitten` command
        # can be used without having to pass `--to <socket>` but remain invisible
        # to the user.
        active_win_pid = ui.active_window().app.pid
        sock = _sock_memo(active_win_pid)
        if sock:
            run_kitten_client(sock, ["action", self._name_, *args])
        else:
            if not self.key_combo:
                warn_msg = (
                    f"No known binding for command {self._name_!r}.\n"
                    "Commands without default key binds will only work when"
                    " kitty has a remote control socket open and Talon knows"
                    " about it. Please set `user.kitty_rpc_socket` in your"
                    " Talon config, make sure it matches the value of the"
                    " `listen_on` directive in your kitty.conf, and that"
                    " `allow_remote_control` is enabled."
                )
                app.notify(
                    title="Talon: kitty",
                    subtitle="Warning: unbound action key",
                    body=warn_msg,
                    sound=True,
                )
            else:
                actions.key(
                    self.key_combo.format(
                        kitty_mod=settings.get("user.kitty_terminal_mod")
                    )
                )


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
    # Novel commands just for kitty
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

    def kitten_insert(kitten: str):
        """Insert `kitten <kitten_name>` into the command line to run kittens
        other than the RPC kitten.

        A list of kittens can be found by running `kitten -h`, using the voice
        command "kitten help," or, for the most info, in the docs at:
        https://sw.kovidgoyal.net/kitty/kittens_intro/

        Stops short of inserting "enter" so you can make sure the kitten you
        intended to run is the one on the command line.
        """
        match kitten:
            case "I cat" | "eye cat":
                kitten = "icat"
            case "S S H":
                kitten = "ssh"
            case "hyperlinked grip":
                kitten = "hyperlinked-grep"
            case "at":
                kitten = "@"
            case "help":
                kitten = "--help"
            # TODO: "diff" is not consistently recognized (at least on my gear),
            # sometimes registering as "iff" or "di."
        actions.insert("kitten ")
        # As of May 2025, all built-in kitten names are kebab-cased.
        actions.user.insert_formatted(kitten, "DASH_SEPARATED")
        actions.key("space")


@ctx.action_class("app")
class AppActions:
    # Implement app.tabs
    def tab_open():
        KittyCmdMap.new_tab.send_command()

    def tab_previous():
        KittyCmdMap.previous_tab.send_command()

    def tab_next():
        KittyCmdMap.close_tab.send_command()

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
