from user.pokey_talon.code.terms import SELECT, TELEPORT, DELETE, FIND
from talon import Context, actions, ui, Module, app, clip
# TODO A lot of these could be supported by supporting a proper "pop back"
# Would basically use the same logic that is used for updating token ranges
mod.list("simple_decorative_action", desc="Supported actions for decorative navigation")
ctx.lists["self.simple_decorative_action"] = {
    # Accepts any single extent
    TELEPORT: "decorative-navigation.moveCursor",
    "cut": "decorative-navigation.cut",
    "copy": "decorative-navigation.copy",
    DELETE: "decorative-navigation.delete",
    FIND: "decorative-navigation.findInFile",
    f"{FIND} last": "decorative-navigation.findBackwardsInFile",
    f"{FIND} all": "decorative-navigation.findAll",
    "fold": "decorative-navigation.fold",
    "cursor": "decorative-navigation.addCursorAt",
    "cursor all": "decorative-navigation.addCursorToAllLines",
    "remove cursor": "decorative-navigation.removeCursor",
    "phones": "phones",
    # Accepts only single token
    "rename": "decorative-navigation.rename",
    "ref show": "decorative-navigation.showReferences",
    "def show": "decorative-navigation.showDefinition",
    "hover show": "decorative-navigation.showHover",
    "act up": "decorative-navigation.scrollToTop",
    "act eat": "decorative-navigation.scrollToMid",
    "act down": "decorative-navigation.scrollToBottom",
    # Accepts position
    "paste": "decorative-navigation.paste",
}

    # Require 2 extents of any kind, but prob best to assume second extend is
    # same type as first, and need to explicitly say "token" if you want to use
    # a token for the second one if the first is not
    # Note: these should actually be of the form "swap <range> with"
    "swap": "decorative-navigation.swap",
    # Require 1 extent of any kind and 1 position, but prob best to assume
    # the position is same type as extent, and need to explicitly say "token"
    # if you want to use a token for the second one if the first is not
    "use": "decorative-navigation.use",
    # Require 1 extent of any kind, and 1 format string (eg "camel foo bar",
    # "phrase hello world" etc, "spell air bat cap")
    # Note: these should actually be of the form "replace <range> with"
    # Could also except a second extent, and that would replace it with that
    # extent
    "replace with": "decorative-navigation.replaceWith",
    # Require 1 extent of any kind, and 1 format type (eg camel, uppercase,
    # phrase etc)
    # Note: these should actually be of the form "reformat <range> as"
    "reformat as": "decorative-navigation.reformatAs",

"<user.search_engine>"