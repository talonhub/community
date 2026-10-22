from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.tag(
    "unix_utilities", desc="tag for enabling unix utility commands in your terminal"
)

# 1. utilities


mod.list("unix_utility", desc="A common utility command")

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
