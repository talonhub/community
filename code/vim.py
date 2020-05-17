# This is largely modeled on vimspeak: https://github.com/AshleyF/VimSpeak
# XXX - probably a lot of the captures could be cleaned up?
# XXX - the old vim speak special characters needs to be replaced to a the
#       existing talon ones
# XXX - finish adding the visual commands, for instance the surround
#       commands for visual mode
# XXX - add visual to upper and lower commands
# XXX - Add support for ordinal motions: "delete 5th word","find second <char>"
# XXX - Support more complext yanking into registers

from talon import Context, Module, actions, ui

mod = Module()
ctx = Context()

ctx.lists["self.vim_surround_targets"] = {
    "stars": "*",
    "asterisks": "*",
    "word": "w",
    "big word": "W",
    "block": "b",
    "big block": "B",
    # Match Talon naming
    "dubstring": '"',
    "dub string": '"',
    "dubquotes": '"',
    "dub quotes": '"',
    "double quotes": '"',
    # Match Talon naming
    "quotes": "'",
    "string": "'",
    "single quotes": "'",
    "loose parens": "(",
    "loose parenthesis": "(",
    "loose angle brackets": "<",
    "loose curly braces": "{",
    "loose braces": "{",
    "loose square brackets": "[",
    "loose brackets": "[",
    "tight parens": ")",
    "tight parenthesis": ")",
    "tight angle brackets": ">",
    "tight curly braces": "}",
    "tight braces": "}",
    "tight square brackets": "]",
    "tight brackets": "]",
    "parens": ")",
    "parenthesis": ")",
    "angle brackets": ">",
    "angles": ">",
    "curly braces": "}",
    "braces": "}",
    "square brackets": "]",
    "squares": "]",
    "brackets": "]",
    "backticks": "`",
    "sentence": "s",
    "paragraph": "p",
    "space": "  ",  # double spaces is required because surround gets confused
    "spaces": "  ",
    "tags": "t",
    "h1 tags": "<h1>",
    "h2 tags": "<h2>",
    "div tags": "<div>",
    "bold tags": "<b>",
}

ctx.lists["self.vim_counted_action_verbs"] = {
    "after": "a",
    "append": "a",
    "after line": "A",
    "append line": "A",
    "insert": "i",
    "insert before line": "I",
    "insert line": "I",
    "insert column zero": "gI",
    # "open": "o",  # conflicts too much with other commands
    "open below": "o",
    "open above": "O",
    "substitute": "s",
    "substitute line": "S",
    "undo": "u",
    "undo line": "U",
    # XXX - fix this control char
    "redo": "<C-r>",
    "erase": "x",
    "erase reversed": "X",
    "erase back": "X",
    "put": "p",
    "put below": "p",
    "paste below": "p",
    "put before": "P",
    "paste before": "P",
    "put above": "P",
    "paste above": "P",
    "repeat": ".",
    # XXX - fix these control characters
    "scroll up": "<C-y>",
    "scroll down": "<C-e>",
    "page down": "<C-f>",
    "page up": "<C-b>",
    "half page down": "<C-d>",
    "half page up": "<C-u>",
    "indent line": ">>",
    "unindent line": "<<",
    "toggle case": "~",
    #    "comment line",             @"\\\",
    #    "comment lines",            @"\\\",
    #    "uncomment line",           @"\\\",
    #    "uncomment lines",          @"\\\",
    "scroll left": "zh",
    "scroll right": "zl",
    "scroll half screen left": "zH",
    "scroll half screen right": "zL",
    "scroll start": "zs",
    "scroll end": "ze",
    "play again": "@@",
}

ctx.lists["self.vim_jump_range"] = {
    "jump to line of": "'",
    "jump to character of": "`",
}

ctx.lists["self.vim_jump_verbs"] = {
    "start of last selection": "<",
    "end of last selection": ">",
    "latest jump": "'",
    "last exit": '"',
    "last insert": "^",
    "last change": ".",
}

# XXX see about replacing the play word with something that doesn't conflict
# with an existing talon grammar
ctx.lists["self.vim_counted_actions_args"] = {
    "play macro": "@",  # takes char arg
}

ctx.lists["self.vim_command_verbs"] = {
    "change": "c",
    "delete": "d",
    "indent": ">",
    "unindent": "<",
    "an indent": "<",
    "un indent": "<",
    "join": "J",
    "filter": "=",
    "put": "p",
    "paste": "p",
    "undo": "u",
    # XXX - this conflicts with default talon 'yank' alphabet for 'y' key
    "yank": "y",
    "copy": "y",
    "fold": "zf",
    "format": "gq",
}

ctx.lists["self.vim_motion_verbs"] = {
    "back": "b",
    "back word": "b",
    "big back": "B",
    "big back word": "B",
    # XXX - this conflicts with default talon 'end' key pressing
    "end": "e",
    "end word": "e",
    "big end": "E",
    "word": "w",
    "words": "w",
    "big word": "W",
    "big words": "W",
    "back end": "ge",
    "back end": "ge",
    "back big end": "gE",
    # XXX - see if there's a way to replaces with normal arrow keys
    "left": "h",
    "down": "j",
    "up": "k",
    "right": "l",
    "next": "n",
    "next reversed": "N",
    "previous": "N",
    "column zero": "0",
    "column": "|",
    "start of line": "^",
    "end of line": "$",
    "search under cursor": "*",
    "search under cursor reversed": "#",
    "again": ";",
    "again reversed": ",",
    "down sentence": ")",
    "sentence": ")",
    "up sentence": "(",
    "down paragraph": "}",
    "paragraph": "}",
    "up paragraph": "{",
    "start of next section": "]]",
    "start of previous section": "[[",
    "end of next section": "][",
    "end of previous section": "[]",
    "matching": "%",
    "down line": "+",
    "up line": "-",
    "first character": "_",
    "cursor home": "H",
    "cursor middle": "M",
    "cursor last": "L",
    "start of document": "gg",
    "start of file": "gg",
    "top of document": "gg",
    "top of file": "gg",
    "end of document": "G",
    "end of file": "G",
    # XXX - these need to be keys
    "retrace movements": "ctrl-o",
    "retrace movements forward": "ctrl-i",
}

# all of these motions take a character argument
ctx.lists["self.vim_motion_verbs_with_character"] = {
    "jump to mark": "'",
    "find": "f",
    "find reversed": "F",
    "till": "t",
    "till reversed": "T",
}

# all of these motions take a phrase argument
ctx.lists["self.vim_motion_verbs_with_phrase"] = {
    "search": "/",
    "search reversed": "?",
}

ctx.lists["self.vim_text_object_count"] = {
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

ctx.lists["self.vim_text_object_range"] = {
    "inner": "i",
    "inside": "i",
    "around": "a",
    "this": "a",
}

ctx.lists["self.vim_text_object_select"] = {
    "word": "w",
    "words": "w",
    "big word": "W",
    "big words": "W",
    "block": "b",
    "blocks": "b",
    "big block": "B",
    "big blocks": "B",
    # Match talon naming (vimspeak used 'quote' for ")
    "dubquote": '"',
    "dub quote": '"',
    "double quotes": '"',
    # Match talon naming
    "quote": "'",
    "single quotes": "'",
    "ticks": "'",
    "parens": "(",
    "parenthesis": "(",
    "angle brackets": "<",
    # These are pluralized because of how you speak vim grammars
    # ex: yank inside braces
    "curly braces": "{",
    "braces": "{",
    "square brackets": "[",
    "squares ": "[",
    "brackets": "[",
    "backticks": "`",
    "sentence": "s",
    "sentences": "s",
    "paragraph": "p",
    "paragraphs": "p",
    "tag block": "t",
}

mod.tag("vim", desc="a tag to load various vim plugins")
mod.list("vim_command_verbs", desc="VIM commands")
mod.list("vim_counted_motion_verbs", desc="Counted VIM motion verbs")
mod.list("vim_counted_action_verbs", desc="Counted VIM action verbs")
mod.list("vim_normal_counted_action", desc="Normal counted VIM actions")
mod.list("vim_motion_verbs", desc="Non-counted VIM motions")
mod.list("vim_motion_verbs_with_character", desc="VIM motion verbs with char arg")
mod.list("vim_motion_verbs_with_phrase", desc="VIM motion verbs with phrase arg")
mod.list("vim_motion_verbs_all", desc="All VIM motion verbs")
mod.list("vim_text_object_count", desc="VIM text object counting")
mod.list("vim_text_object_range", desc="VIM text object ranges")
mod.list("vim_text_object_select", desc="VIM text object selections")
mod.list("vim_jump_range", desc="VIM jump ranges")
mod.list("vim_jump_verbs", desc="VIM jump verbs")
mod.list("vim_jump_targets", desc="VIM jump targets")
mod.list("vim_normal_counted_command", desc="Counted normal VIM commands")
mod.list("vim_select_motion", desc="VIM visual mode selection motions")
mod.list("vim_surround_targets", desc="VIM surround plugin targets")
mod.list("vim_any", desc="All vim commands")


@mod.capture
def vim_surround_targets(m) -> str:
    "Returns a string"


@mod.capture
def vim_select_motion(m) -> str:
    "Returns a string"


@mod.capture
def vim_counted_action_verbs(m) -> str:
    "Returns a string"


@mod.capture
def vim_normal_counted_action(m) -> str:
    "Returns a string"


@mod.capture
def vim_jump_targets(m) -> str:
    "Returns a string"


@mod.capture
def vim_jump_verbs(m) -> str:
    "Returns a string"


@mod.capture
def vim_jump_range(m) -> str:
    "Returns a string"


@mod.capture
def vim_text_object_count(m) -> str:
    "Returns a string"


@mod.capture
def vim_text_object_range(m) -> str:
    "Returns a string"


@mod.capture
def vim_text_object_select(m) -> str:
    "Returns a string"


@mod.capture
def vim_command_verbs(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_counted_motion_verbs(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motion_verbs(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motion_verbs_with_upper_character(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motion_verbs_with_character(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motion_verbs_with_phrase(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motion_verbs_all(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_any(m) -> str:
    "Any one key"


@mod.capture
def vim_text_objects(m) -> str:
    "Returns a string"


@mod.capture
def vim_unranged_surround_text_objects(m) -> str:
    "Returns a string"


@mod.capture
def vim_normal_counted_command(m) -> str:
    "Returns a string"


@ctx.capture(rule="{self.vim_text_object_select}")
def vim_text_object_select(m) -> str:
    "Returns a string"
    return m.vim_text_object_select


@ctx.capture(rule="{self.vim_text_object_range}")
def vim_text_object_range(m) -> str:
    "Returns a string"
    return m.vim_text_object_range


@ctx.capture(rule="{self.vim_text_object_count}")
def vim_text_object_count(m) -> str:
    "Returns a string"
    return m.vim_text_object_count


@ctx.capture(rule="{self.vim_command_verbs}")
def vim_command_verbs(m) -> str:
    return m.vim_command_verbs


@ctx.capture(rule="{self.vim_motion_verbs}")
def vim_motion_verbs(m) -> str:
    return m.vim_motion_verbs


@ctx.capture(
    rule="{self.vim_motion_verbs_with_character} (ship|upper|uppercase) <user.letter>$"
)
def vim_motion_verbs_with_upper_character(m) -> str:
    return m.vim_motion_verbs_with_character + "".join(list(m)[2:]).upper()


@ctx.capture(
    rule="{self.vim_motion_verbs_with_character} (<user.letter>|<user.number>|<user.symbol>)$"
)
# @ctx.capture(rule='{self.vim_motion_verbs_with_character} <user.any>')
def vim_motion_verbs_with_character(m) -> str:
    return m.vim_motion_verbs_with_character + "".join(list(m)[1:])


@ctx.capture(rule="{self.vim_motion_verbs_with_phrase} <phrase>")
def vim_motion_verbs_with_phrase(m) -> str:
    return "".join(list(m.vim_motion_verbs_with_phrase + m.phrase))


@ctx.capture(
    rule="(<self.vim_motion_verbs>|<self.vim_motion_verbs_with_character>|<self.vim_motion_verbs_with_upper_character>|<self.vim_motion_verbs_with_phrase>)$"
)
def vim_motion_verbs_all(m) -> str:
    return "".join(list(m))


@ctx.capture(rule="{self.vim_counted_action_verbs}")
def vim_counted_action_verbs(m) -> str:
    return m.vim_counted_action_verbs


@ctx.capture(rule="[<self.number>] <self.vim_motion_verbs_all>$")
def vim_counted_motion_verbs(m) -> str:
    return "".join(list(m))


@ctx.capture(rule="{self.vim_jump_range}")
def vim_jump_range(m) -> str:
    return m.vim_jump_range


@ctx.capture(rule="{self.vim_jump_verbs}")
def vim_jump_verbs(m) -> str:
    return m.vim_jump_verbs


@ctx.capture(rule="{self.vim_surround_targets}")
def vim_surround_targets(m) -> str:
    return m.vim_surround_targets


@ctx.capture(rule="<self.vim_jump_range> <self.vim_jump_verbs>$")
def vim_jump_targets(m) -> str:
    return "".join(list(m))


@ctx.capture(
    rule="[<self.vim_text_object_count>] <self.vim_text_object_range> <self.vim_text_object_select>$"
)
def vim_text_objects(m) -> str:
    return "".join(list(m))


# when speaking adding in the object ranges a little bit annoying, so it's a
# little bit and more natural to just assume that you mean around if you didn't
# say anything
@ctx.capture(rule="[<self.vim_text_object_count>] <self.vim_text_object_select>$")
def vim_unranged_surround_text_objects(m) -> str:
    if len(list(m)) == 1:
        return "a" + "".join(list(m))
    else:
        return "".join(list(m)[0:1]) + "a" + "".join(list(m)[1:])


@ctx.capture(
    rule="[<self.number>] <self.vim_command_verbs> (<self.vim_motion_verbs_all> | <self.vim_text_objects> | <self.vim_jump_targets>)$"
)
def vim_normal_counted_command(m) -> str:
    return "".join(list(m))


@ctx.capture(rule="[<self.number>] <self.vim_counted_action_verbs>$")
def vim_normal_counted_action(m) -> str:
    return "".join(list(m))


@ctx.capture(
    rule="[<self.number>] (<self.vim_motion_verbs> | <self.vim_text_objects> | <self.vim_jump_targets>)$"
)
def vim_select_motion(m) -> str:
    return "".join(list(m))


# XXX - this doesn't work yet, but all eventually final everything through here
# so that we can detect/change the mode
@mod.action_class
class Actions:
    def run_vim_cmd(words: list):
        """Insert an abbreviation"""
        #        for word in words:
        #            actions.insert(word)
        print(words)
        vim_mode = VimMode()
        mode = vim_mode.get_active_mode()
        rpc_path = vim_mode.get_active_rpc()
        if mode is not None:
            print(mode)
        if rpc_path is not None:
            print(rpc_path)


class VimMode:
    vim_modes = {
        "n": "Normal",
        "no": "N Operator Pending",
        "v": "Visual",
        "V": "V Line",
        "^V": "V-Block",
        "s": "Select",
        "S": "S·Line",
        "i": "Insert",
        "R": "Replace",
        "Rv": "V·Replace",
        "c": "Command",
        "cv": "Vim Ex",
        "ce": "Ex",
        "r": "Prompt",
        "rm": "More",
        "r?": "Confirm",
        "!": "Shell",
    }

    def __init__(self):
        # list of all vim instances talon is aware of
        self.vim_instances = []
        self.current_mode = None
        self.current_rpc = None

    def is_normal_mode(self, mode):
        return mode[0] == "n"

    def is_visual_mode(self, mode):
        return mode == "v" or mode == "V" or mode == "^V"

    def get_active_mode(self):
        title = ui.active_window().title
        mode = None
        if "MODE:" in title:
            mode = title.split("MODE:")[1].split(" ")[0]
            if mode not in self.vim_modes.keys():
                return None
            self.current_mode = mode
        return mode

    # XXX - currently only support UDS named pipes
    def get_active_rpc(self):
        title = ui.active_window().title
        if "RPC" in title:
            named_pipe = title.split("RPC:")[1].split(" ")[0]
            return named_pipe
        return None

    # if neovim RPC is supported we use it
    # otherwise we simply use keyboard binding combinations
    def set_mode(self, mode):
        print("Set vim mode")
