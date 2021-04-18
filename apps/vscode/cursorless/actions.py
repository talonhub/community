from user.pokey_talon.code.terms import SELECT, TELEPORT, DELETE, FIND
from talon import Context, actions, ui, Module, app, clip

mod = Module()

ctx = Context()
ctx.matches = r"""
app: vscode
"""

# TODO A lot of these could be supported by supporting a proper "pop back"
# Would basically use the same logic that is used for updating token ranges
mod.list("simple_cursorless_action", desc="Supported actions for cursorless navigation")
ctx.lists["self.simple_cursorless_action"] = {
    # Accepts any single extent
    "spring": "setSelection",
    SELECT: "setSelection",
    "pree": "setSelectionBefore",
    "post": "setSelectionAfter",
    DELETE: "delete",
    # "sort": "sortLines",
    # "cut": "cut",
    # "copy": "copy",
    # FIND: "findInFile",
    # f"{FIND} last": "findBackwardsInFile",
    # f"{FIND} all": "findAll",
    # "fold": "fold",
    # "cursor": "addCursorAt",
    # "cursor all": "addCursorToAllLines",
    # "remove cursor": "removeCursor",
    # "tab": "indent",
    # "retab": "dedent",
    # "comment": "comment",
    # "github open": "openInGithub",
    # "smear": "cloneLineDown",
    # # Accepts only single token
    # "rename": "rename",
    # "ref show": "showReferences",
    # "def show": "showDefinition",
    # "hover show": "showHover",
    # "act up": "scrollToTop",
    # "act eat": "scrollToMid",
    # "act down": "scrollToBottom",
    # # Accepts position
    # "paste": "paste",
}

{
    # Require 2 extents of any kind, but prob best to assume second extend is
    # same type as first, and need to explicitly say "token" if you want to use
    # a token for the second one if the first is not
    # Note: these should actually be of the form "swap <range> with"
    "swap": "swap",
    # Require 1 extent of any kind and 1 position, but prob best to assume
    # the position is same type as extent, and need to explicitly say "token"
    # if you want to use a token for the second one if the first is not
    "use": "use",
    # Require 1 extent of any kind, and 1 format string (eg "camel foo bar",
    # "phrase hello world" etc, "spell air bat cap")
    # Note: these should actually be of the form "replace <range> with"
    # Could also except a second extent, and that would replace it with that
    # extent
    "replace with": "replaceWith",
    # Require 1 extent of any kind, and 1 format type (eg camel, uppercase,
    # phrase etc)
    # Note: these should actually be of the form "reformat <range> as"
    "reformat as": "reformatAs",
}
"<user.search_engine>"
"phones"