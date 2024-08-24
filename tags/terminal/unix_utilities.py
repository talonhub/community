from talon import Context, Module, actions

from ...core.user_settings import get_list_from_csv

ctx = Context()
mod = Module()

mod.tag(
    "unix_utilities", desc="tag for enabling unix utility commands in your terminal"
)

# 1. utilities

# Do not edit this dictionary. It is just used to initially populate 'settings/unix_utilities.csv'.
# Edit that file instead if you want to customize your commands.
default_unix_utilities = {
    "ark": "awk",
    "base sixty four decode": "base64 -d",
    "base sixty four": "base64",
    "concat": "cat",
    "change mode recurse": "chmod -R",
    "change mode": "chmod",
    "change owner recurse": "chown -R",
    "change owner": "chown",
    "curl": "curl",
    "cut": "cut",
    "disk free human": "df -h",
    "disk free": "df",
    "dig": "dig",
    "disk usage human": "du -h",
    "disk usage": "du",
    "echo": "echo",
    "false": "false",
    "find": "find",
    "grab here": "grep -Hirn",
    "grab": "grep",
    "head": "head",
    "harp top": "htop",
    "I D user": "id -u",
    "I D": "id",
    "less": "less",
    "link soft": "ln -s",
    "link": "ln",
    "M D five sum": "md5sum",
    "make dear": "mkdir",
    "paste": "paste",
    "print format": "printf",
    "work dear": "pwd",
    "reverse": "rev",
    "are sync": "rsync",
    "said": "sed",
    "sequence": "seq",
    "shah two fifty six sum": "sha256sum",
    "sleep": "sleep",
    "sort human": "sort -h",
    "sort numeric": "sort -n",
    "sort reverse": "sort -r",
    "sort unique": "sort -u",
    "sort": "sort",
    "S S H": "ssh",
    "stat": "stat",
    "pseudo": "sudo",
    "tail follow": "tail -f",
    "tail": "tail",
    "tea append": "tee -a",
    "tea": "tee",
    "touch": "touch",
    "translate delete": "tr -d",
    "translate": "tr",
    "true": "true",
    "unique count": "uniq -c",
    "unique": "uniq",
    "word count characters": "wc -c",
    "word count lines": "wc -l",
    "word count": "wc",
    "who": "who",
    "who am I": "whoami",
}

unix_utilities = get_list_from_csv(
    "unix_utilities.csv",
    headers=("command", "spoken"),
    default=default_unix_utilities,
)

mod.list("unix_utility", desc="A common utility command")
ctx.lists["self.unix_utility"] = unix_utilities

# 2. arguments

default_unix_arguments = {
    "all": "all",
    "debug": "debug",
    "file": "file",
    "force": "force",
    "help": "help",
    "output": "output",
    "quiet": "quiet",
    "recursive": "recursive",
    "silent": "silent",
    "user": "user",
    "verbose": "verbose",
    "version": "version",
}

unix_arguments = get_list_from_csv(
    "unix_arguments.csv",
    headers=("argument", "spoken"),
    default=default_unix_arguments,
)

mod.list("unix_argument", desc="Command-line options and arguments.")
ctx.lists["self.unix_argument"] = unix_arguments


@mod.capture(rule="{user.unix_argument}+")
def unix_arguments(m) -> str:
    """A non-empty sequence of unix command arguments, preceded by a space."""
    return " --".join([""] + m.unix_argument_list)


@mod.capture(rule="( {user.unix_argument} | <user.text> )")
def unix_free_form_argument(m) -> str:
    """An argument name in kebab-case, with defined arguments being preferred."""
    return actions.user.formatted_text(m, "DASH_SEPARATED")
