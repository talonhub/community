import enum
import os
import re
import subprocess
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from collections.abc import Iterable, Sequence
from typing import cast

from talon import actions, app, settings, ui

XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME")
XDG_CONFIG_DIRS = os.environ.get("XDG_CONFIG_DIRS")

kitty_config_locations: tuple[Path, ...] = (
    Path(f"{XDG_CONFIG_HOME}/kitty/kitty.conf"),
    Path("~/.config/kitty/kitty.conf"),
    Path(f"{XDG_CONFIG_DIRS}/kitty/kitty.conf"),
)


def read_kitty_conf() -> list[str] | None:
    for loc in kitty_config_locations:
        loc = loc.expanduser()
        if os.access(loc, os.R_OK):
            with open(loc, "r") as f:
                return f.readlines()


def parse_kitty_conf(conf: Sequence[str]) -> dict[str, str | list[tuple[str, ...]]]:
    # map_re = re.compile(r'^\s*map\s+(?P<bind>[^# ]+)\s+(?P<cmd>[^#]+)')
    # listen_on_re = re.compile(r'^\s*listen_on\s+([^# ]+)')
    settings = {}
    for line in conf:
        # Skip empty lines and comments.
        # It's worth noting kitty's own config parser doesn't allow in-line
        # comments, as colors are given as '#<hex><hex><hex>' strings.
        if not line or line.lstrip(" \t")[0] == "#":
            continue
        # Merge consecutive whitespace into a single tab. This has the weakness
        # that a quoted argument that deliberately has consecutive whitespace
        # will also be mangled, but for now I'm not concerned with that corner-
        # case.
        deduplicated = '\t'.join(
            s for s in re.split(r'\s+', line, maxsplit=3) if s
        ).rstrip("\n\r")
        # Skip if that created an empty line
        if not deduplicated:
            continue
        # Re-split on the tabs we created
        parts = deduplicated.split("\t")
        # kitty.conf syntax is verb-initial. With map commands (the ones we're
        # most interested in), the key combo is the second part and the action
        # is the remainder. The action may have spaces, which is why we used
        # tabs above.
        if parts[0] in settings:
            cur = settings[parts[0]]
            if not isinstance(cur, list):
                settings[parts[0]] = [cur, tuple(parts[1:])]
            else:
                settings[parts[0]].append(tuple(parts[1:]))
        else:
            if len(parts[1:]) == 1:
                settings[parts[0]] = parts[1]
            else:
                settings[parts[0]] = tuple(parts[1:])
    return settings


KITTY_CONF = {}


def _reload_conf():
    global KITTY_CONF
    if conf := read_kitty_conf():
        KITTY_CONF = parse_kitty_conf(conf)

app.register("ready", _reload_conf)


def parse_map_cmds(
    maps: Sequence[tuple[str, ...]]
) -> list[tuple[str, str, tuple[str, ...]]]:
    """kitty.conf maps look like `map <keys> <command>`. If we're to construct
    a CmdMap, we want `<command> <keys>`, s/>/ /g and s/+/-/g, and wrap
    'kitty_mod' in braces.
    Also, `parse_kitty_conf` splits the command, too, but we'll want just one string.
    """
    out: list[tuple[str, str, tuple[str, ...]]] = []
    for key, *cmd in maps:
        if cmd[0] == "no_op":
            continue
        out.append(
            (
                cmd[0],
                (
                    key.replace("kitty_mod", "{kitty_mod}")
                    .replace(">", " ")
                    .replace("+", "-")
                ),
                tuple(cmd[1:]),
            )
        )
    return out


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


def kitty_mod() -> str:
    """Fetch the user's configured `kitty_terminal_mod`, if set.

    Override this in your own settings:
        -
        settings():
            user.kitty_terminal_mod = <combo that matches your kitty.conf>

    This has to be a function to defer fetching the value until it's definitely
    been read by Talon.
    """
    return (
        cast(str, KITTY_CONF.get("kitty_mod", ""))
        or settings.get("user.kitty_terminal_mod")
    )


@cache
def _sock_memo(active_win_pid: int) -> str:
    """Memoize formatted socket paths for each kitty PID."""
    # Possibly a premature optimization: the time to return (measured by
    # ipython's %timeit) was over 4.5x faster vs doing the string formatting
    # every time. Sounds pretty cool... but 4.5 * 35.3ns is still only 160ns.
    if not settings.get("user.kitty_use_rpc"):
        return ""
    sock = (
        cast(str, KITTY_CONF.get("listen_on", ""))
        or settings.get("user.kitty_rpc_socket")
    )
    if sock and not settings.get("user.kitty_rpc_socket_verbatim"):
        if "{kitty_pid}" in sock:
            sock = sock.format(kitty_pid=active_win_pid)
        else:
            sock = sock + f"-{active_win_pid}"
    return sock


# Clear the cache if Talon reloads, just in case kitty_rpc_socket was one of
# the things that changed to trigger the reload.
app.register("ready", _sock_memo.cache_clear)


@dataclass
class MapDirective:
    """Represents the pieces of a `map` directive in kitty.conf"""

    action: str
    key_combo: str
    arguments: tuple[str, ...] = ()

    def reconstruct(self):
        return "map {} {} {}".format(
            self.key_combo.translate(
                str.maketrans({"{": "", "}": "", "-": "+", " ": ">"})
            ),
            self.action,
            " ".join(self.arguments),
        )


class CmdMap(MapDirective, enum.Enum):
    """Initially meant to provide polymorphism to accommodate kitty actions that
    needed things like arguments--a problem better solved by `MapDirective` enum
    members--now this serves mostly to keep the "business" logic from cluttering
    the main python script, where users are likely to look when trying to
    understand commands.

    New subclasses can be declared at runtime, too. This is used to represent
    the user's configuration and merge it with the known defaults.
    """

    def _send_command(self, *args):
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
            run_kitten_client(sock, args)
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
                        kitty_mod=kitty_mod()
                    )
                )

    def send_command(self, *args):
        self._send_command("action", self.action, *self.arguments, *args)

if maps := KITTY_CONF.get("map", None):
    UserCmdMap = CmdMap(
        "UserCmdMap",
        [("_".join((md[0], *md[2])), (*md,)) for md in parse_map_cmds(maps)],
    )
else:
    UserCmdMap = None


# TODO: if rpc is enabled, we can do two things:
# 1) Run `kitty +runpy 'from kitty.config import *;
# print(commented_out_default_config())'` to get a complete list of all default
# key maps (this will need special parsing, since _every_ line starts with #)
# 2) run `kitten @ action debug_config` to get the user's loaded configuration
# (again, needs special parsing).
# Is it worth it..? Two different parsers needed to do what's currently done by
# one and some hardcoding...

# If using `subprocess` for rpc is rejected, we may have to implement the
# json-based rpc protocol and send it directly over the socket.
