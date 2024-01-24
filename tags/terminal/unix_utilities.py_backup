from talon import Context, Module

from ...core.user_settings import get_list_from_csv

ctx = Context()
mod = Module()

mod.tag(
    "unix_utilities", desc="tag for enabling unix utility commands in your terminal"
)

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
