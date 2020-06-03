# Talon VIM - inspired by vimspeak: https://github.com/AshleyF/VimSpeak
# see doc/vim.md
#
# XXX - the old vim speak special characters needs to be replaced to a the
#       existing talon ones
# XXX - Add support for ordinal motions: "delete 5th word","find second <char>"
# XXX - Support more complex yanking into registers
# XXX - add fugitive mode mapping stuff. See :help fugitive
#       most of the vim cmds should be disabled while in there? longer term
#       solution for fugitive should be just adding in win.title changes
#       directly into the project and sending tpope a PR
# XXX - have two version of most lists. "standard" and then "custom", and
#       combine them into the context lists. this should allow people to
#       maintain custom lists without merge conflicts
# XXX - define all the lists separately and then update ctx.lists only once
# XXX - add custom lists of commands for terminal mode enforcement
# XXX - document that visual selection mode implies terminal escape
# XXX - some surround stuff stopped working
# XXX - eventually use nvim RPC to confirm mode changes vs relying on a time
#       delay that is buggy depending on your cpu consumption
# XXX - add setting for disabling local terminal escape when running inside
#       remote vim sessions via ssh, etc
# XXX - need to support other mode changes (command, replace, etc)
# XXX - import and test scenario where the mode isn't listed at all
# XXX - add test cases

import time

from talon import Context, Module, actions, settings, ui

mod = Module()
ctx = Context()

ctx.matches = r"""
win.title:/VIM/
"""

# Based on you using a custom title string like this:
# let &titlestring ='VIM MODE:%{mode()} (%f) %t'
# see doc/vim.md
@ctx.action_class("win")
class win_actions:
    def filename():
        title = actions.win.title()
        result = title.split(")")
        if len(result) > 1:
            result = result[1]
        if "." in result:
            return result
        return ""

    def file_ext():
        return actions.win.filename().split(".")[-1]


ctx.lists["self.vim_arrow"] = {
    "left": "h",
    "right": "l",
    "up": "k",
    "down": "j",
}

# XXX - need to break into normal, visual, etc
ctx.lists["self.vim_counted_actions"] = {
    "after": "a",
    "append": "a",
    "after line": "A",
    "append line": "A",
    "insert": "i",
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
    "paste": "p",
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
    "delete line": "dd",
    "yank line": "Y",
    # "copy line": "Y",
    "scroll left": "zh",
    "scroll right": "zl",
    "scroll half screen left": "zH",
    "scroll half screen right": "zL",
    "scroll start": "zs",
    "scroll end": "ze",
    # XXX - these work from visual mode and normal mode
    "insert before line": "I",
    "insert line": "I",
    "play again": "@@",
    "toggle case": "~",
    # XXX - custom
    "panic": "u",
}

ctx.lists["self.vim_jump_range"] = {
    "jump to line of": "'",
    "jump to character of": "`",
}

ctx.lists["self.vim_jumps"] = {
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

# normal mode commands that require motion, and that are counted
# includes motions and no motions :|
commands_with_motion = {
    # no motions
    "join": "J",
    "filter": "=",  # XXX - not sure about how to use this
    "put": "p",
    "paste": "p",
    "undo": "u",
    "swap case": "~",
    # motions
    "change": "c",
    "delete": "d",
    "indent": ">",
    "unindent": "<",
    "an indent": "<",
    "un indent": "<",
    "yank": "y",  # XXX - conflicts with talon 'yank' alphabet for 'y' key
    # NOTE: If you enable this and yank at the same time, some convenience
    # commands you might setup for automatic copying might get swallowed by
    # vim.py grammars
    "copy": "y",
    "fold": "zf",
    "format": "gq",
    "to upper": "gU",
    "to lower": "gu",
}

# only relevant when in visual mode. these will have some overlap with
# commands  and commands_with_motion above. this is mostly because
# some characters differ, and also in visual mode they don't have motions
visual_commands = {
    # normal overlap
    "change": "c",
    "join": "J",
    "delete": "d",
    "yank": "y",  # XXX - conflicts with talon 'yank' alphabet for 'y' key
    "copy": "y",
    "format": "gq",
    "fold": "zf",
    # some visual differences
    "to upper": "U",
    "to lower": "u",
    "swap case": "~",
    "opposite": "o",
    # counted
    "indent": ">",
    "unindent": "<",
    "an indent": "<",
    "un indent": "<",
}


ctx.lists["self.vim_motion_commands"] = list(
    set().union(commands_with_motion.keys(), visual_commands.keys())
)


ctx.lists["self.vim_motions"] = {
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
    # todo - convenience
    "function start": "[[",
    "funk start": "[[",
    "next function": "]]",
    "next funk": "]]",
}

# all of these motions take a character argument
ctx.lists["self.vim_motions_with_character"] = {
    "jump to mark": "'",
    "find": "f",
    "find reversed": "F",
    "find previous": "F",
    "till": "t",
    "till reversed": "T",
    "till previous": "T",
}

# all of these motions take a phrase argument
ctx.lists["self.vim_motions_with_phrase"] = {
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

# XXX - Should match more wording in vim_surround_targets
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

# Specific to the vim-surround plugin
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


mod.tag("vim", desc="a tag to load various vim plugins")
mod.setting(
    "vim_preserve_insert_mode",
    type=int,
    default=1,
    desc="If normal mode actions are called from insert mode, stay in insert",
)

mod.setting(
    "vim_adjust_modes",
    type=int,
    default=1,
    desc="User wants talon to automatically adjust modes for commands",
)

mod.setting(
    "vim_notify_mode_changes",
    type=int,
    default=0,
    desc="Notify user about vim mode changes as they occur",
)

mod.setting(
    "vim_escape_terminal_mode",
    type=int,
    default=0,
    desc="When set won't limit what motions and commands will pop out of terminal mode",
)
mod.setting(
    "vim_cancel_queued_commands",
    type=int,
    default=1,
    desc="Press escape before issuing commands, to cancel previously queued command that might have been in error",
)

mod.setting(
    "vim_cancel_queued_commands_timeout",
    type=float,
    default=0.3,
    desc="How long to wait in seconds before issuing the real command after canceling",
)

mod.setting(
    "vim_mode_change_timeout",
    type=float,
    default=0.3,
    desc="It how long to wait before issuing commands after a mode change",
)

# Standard VIM motions and action
mod.list("vim_arrow", desc="All vim direction keys")
mod.list("vim_motion_commands", desc="Counted VIM commands with motions")
mod.list("vim_counted_motions", desc="Counted VIM motion verbs")
mod.list("vim_counted_actions", desc="Counted VIM action verbs")
mod.list("vim_normal_counted_action", desc="Normal counted VIM actions")
mod.list("vim_motions", desc="Non-counted VIM motions")
mod.list("vim_motions_with_character", desc="VIM motion verbs with char arg")
mod.list("vim_motions_with_phrase", desc="VIM motion verbs with phrase arg")
mod.list("vim_motions_all", desc="All VIM motion verbs")
mod.list("vim_text_object_count", desc="VIM text object counting")
mod.list("vim_text_object_range", desc="VIM text object ranges")
mod.list("vim_text_object_select", desc="VIM text object selections")
mod.list("vim_jump_range", desc="VIM jump ranges")
mod.list("vim_jumps", desc="VIM jump verbs")
mod.list("vim_jump_targets", desc="VIM jump targets")
mod.list("vim_normal_counted_motion_command", desc="Counted normal VIM commands")
mod.list("vim_select_motion", desc="VIM visual mode selection motions")
mod.list("vim_any", desc="All vim commands")

# Plugin-specific lists
mod.list("vim_surround_targets", desc="VIM surround plugin targets")

# Plugin modes
mod.mode("vim_fugitive", desc="A fugitive mode that exposes git mappings")


@mod.capture
def vim_arrow(m) -> str:
    "An arrow to be converted to vim direction"


@mod.capture
def vim_surround_targets(m) -> str:
    "Returns a string"


@mod.capture
def vim_select_motion(m) -> str:
    "Returns a string"


@mod.capture
def vim_counted_actions(m) -> str:
    "Returns a string"


@mod.capture
def vim_normal_counted_action(m) -> str:
    "Returns a string"


@mod.capture
def vim_jump_targets(m) -> str:
    "Returns a string"


@mod.capture
def vim_jumps(m) -> str:
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
def vim_motion_commands(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motion_command(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_counted_motions(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motions(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motions_with_upper_character(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motions_with_character(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motions_with_phrase(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motions_all(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motions_all_adjust(m) -> str:
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
def vim_normal_counted_motion_command(m) -> str:
    "Returns a string"


@ctx.capture(rule="{self.vim_arrow}")
def vim_arrow(m):
    return m.vim_arrow


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


@ctx.capture(rule="{self.vim_motions}")
def vim_motions(m) -> str:
    return m.vim_motions


@ctx.capture(
    rule="{self.vim_motions_with_character} (ship|upper|uppercase) <user.letter>$"
)
def vim_motions_with_upper_character(m) -> str:
    return m.vim_motions_with_character + "".join(list(m)[2:]).upper()


@ctx.capture(
    rule="{self.vim_motions_with_character} (<user.letter>|<user.number>|<user.symbol>)$"
)
def vim_motions_with_character(m) -> str:
    return m.vim_motions_with_character + "".join(list(m)[1:])


@ctx.capture(rule="{self.vim_motions_with_phrase} <user.text>")
def vim_motions_with_phrase(m) -> str:
    return "".join(list(m.vim_motions_with_phrase + m.text))


@ctx.capture(
    rule="(<self.vim_motions>|<self.vim_motions_with_character>|<self.vim_motions_with_upper_character>|<self.vim_motions_with_phrase>)$"
)
def vim_motions_all(m) -> str:
    return "".join(list(m))


@ctx.capture(
    rule="(<self.vim_motions>|<self.vim_motions_with_character>|<self.vim_motions_with_upper_character>|<self.vim_motions_with_phrase>)$"
)
def vim_motions_all_adjust(m) -> str:
    v = VimMode()
    v.set_any_motion_mode()
    return "".join(list(m))


@ctx.capture(rule="{self.vim_counted_actions}")
def vim_counted_actions(m) -> str:
    return m.vim_counted_actions


@ctx.capture(rule="[<self.number>] <self.vim_motions_all>$")
def vim_counted_motions(m) -> str:
    return "".join(list(m))


@ctx.capture(rule="{self.vim_jump_range}")
def vim_jump_range(m) -> str:
    return m.vim_jump_range


@ctx.capture(rule="{self.vim_jumps}")
def vim_jumps(m) -> str:
    return m.vim_jumps


@ctx.capture(rule="{self.vim_surround_targets}")
def vim_surround_targets(m) -> str:
    return m.vim_surround_targets


@ctx.capture(rule="<self.vim_jump_range> <self.vim_jumps>$")
def vim_jump_targets(m) -> str:
    return "".join(list(m))


@ctx.capture(
    rule="[<self.vim_text_object_count>] <self.vim_text_object_range> <self.vim_text_object_select>$"
)
def vim_text_objects(m) -> str:
    return "".join(list(m))


# XXX - clarify this comment
# when speaking adding in the object ranges a little bit annoying, so it's a
# little bit and more natural to just assume that you mean around if you didn't
# say anything
@ctx.capture(rule="[<self.vim_text_object_count>] <self.vim_text_object_select>$")
def vim_unranged_surround_text_objects(m) -> str:
    if len(list(m)) == 1:
        return "a" + "".join(list(m))
    else:
        return "".join(list(m)[0:1]) + "a" + "".join(list(m)[1:])


@ctx.capture(rule="{self.vim_motion_commands}$")
def vim_motion_commands(m) -> str:
    v = VimMode()
    if v.is_visual_mode():
        if str(m) in visual_commands:
            return visual_commands[str(m)]
    # Note this throws away commands that matched visual mode only stuff,
    # because if not in visual mode already, there is no selection anyway so
    # the command is moot
    elif str(m) not in commands_with_motion:
        print("no match for {}".format(str(m)))
        return None

    v.set_normal_mode()
    return commands_with_motion[str(m)]


@ctx.capture(
    rule="[<self.number>] <self.vim_motion_commands> [(<self.vim_motions_all> | <self.vim_text_objects> | <self.vim_jump_targets>)]$"
)
def vim_normal_counted_motion_command(m) -> str:
    return "".join(list(m))


@ctx.capture(rule="[<self.number>] <self.vim_counted_actions>$")
def vim_normal_counted_action(m) -> str:
    # XXX - may need to do action-specific mode checking
    v = VimMode()
    v.cancel_queued_commands()
    if m.vim_counted_actions == "u":
        # undo doesn't work with ctrl-o it seems
        v.set_any_motion_mode_np()
    else:
        v.set_any_motion_mode()
    return "".join(list(m))


@ctx.capture(
    rule="[<self.number>] (<self.vim_motions> | <self.vim_text_objects> | <self.vim_jump_targets>)$"
)
def vim_select_motion(m) -> str:
    return "".join(list(m))


# These are actions you can call from vim.talon via `user.method_name()` in
# order to modify modes, run commands in specific modes, etc
@mod.action_class
class Actions:
    def vim_set_normal_mode():
        """set normal mode"""
        v = VimMode()
        v.set_normal_mode(auto=False)

    def vim_set_normal_mode_exterm():
        """set normal mode and don't preserve the previous mode"""
        v = VimMode()
        v.set_normal_mode_exterm()

    def vim_set_normal_mode_np():
        """set normal mode and don't preserve the previous mode"""
        v = VimMode()
        v.set_normal_mode_np(auto=False)

    def vim_set_visual_mode():
        """set visual mode"""
        v = VimMode()
        v.set_visual_mode()

    def vim_set_insert_mode():
        """set insert mode"""
        v = VimMode()
        v.set_insert_mode()

    def vim_set_terminal_mode():
        """set terminal mode"""
        v = VimMode()
        v.set_terminal_mode()

    def vim_insert_mode(cmd: str):
        """run a given list of commands in normal mode, preserve mode"""
        v = VimMode()
        v.set_insert_mode()
        actions.insert(cmd)

    def vim_insert_mode_np(cmd: str):
        """run a given list of commands in normal mode, don't preserve"""
        v = VimMode()
        v.set_insert_mode_np()
        actions.insert(cmd)

    def vim_normal_mode(cmd: str):
        """run a given list of commands in normal mode, preserve INSERT"""
        v = VimMode()
        v.set_normal_mode()
        actions.insert(cmd)

    def vim_normal_mode_np(cmd: str):
        """run a given list of commands in normal mode, don't preserve
        INSERT"""
        v = VimMode()
        v.set_normal_mode_np()
        actions.insert(cmd)

    def vim_normal_mode_exterm(cmd: str):
        """run a given list of commands in normal mode, don't preserve INSERT,
        escape from terminal mode"""
        v = VimMode()
        v.set_normal_mode_exterm()
        actions.insert(cmd)

    def vim_normal_mode_key(cmd: str):
        """press a given key in normal mode"""
        v = VimMode()
        v.set_normal_mode()
        actions.key(cmd)

    def vim_normal_mode_exterm_key(cmd: str):
        """press a given key in normal mode, and escape terminal"""
        v = VimMode()
        v.set_normal_mode_exterm()
        actions.key(cmd)

    def vim_normal_mode_keys(keys: str):
        """press a given list of keys in normal mode"""
        v = VimMode()
        v.set_normal_mode()
        for key in keys:
            # print(key)
            actions.key(key)

    def vim_visual_mode(cmd: str):
        """run a given list of commands in visual mode"""
        v = VimMode()
        v.set_visual_mode()
        actions.insert(cmd)

        """run a given list of commands in insert mode"""
        v = VimMode()
        v.set_insert_mode()
        actions.insert(cmd)

    # Sometimes the .talon file won't know what mode to run something in, just
    # that it needs to be a mode that supports motions like normal and visual.
    def vim_any_motion_mode(cmd: str):
        """run a given list of commands in normal mode"""
        v = VimMode()
        v.set_any_motion_mode()
        actions.insert(cmd)

    def vim_any_motion_mode_key(cmd: str):
        """run a given list of commands in normal mode"""
        v = VimMode()
        v.set_any_motion_mode()
        actions.key(cmd)


class VimMode:
    # mode ids represent more generic statusline mode() values. see :help mode()
    NORMAL = 1
    VISUAL = 2
    INSERT = 3
    TERMINAL = 4

    # XXX - not really necessary here, but just used to sanity check for now
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
        "t": "Terminal",
    }

    def __init__(self):
        # list of all vim instances talon is aware of
        self.vim_instances = []
        self.current_rpc = None
        self.normal_modes = ["n"]
        self.visual_modes = ["v", "V", "^V"]
        self.current_mode = self.get_active_mode()

    def is_normal_mode(self):
        return self.current_mode == "n"

    def is_visual_mode(self):
        return self.current_mode in ["v", "V", "^V"]

    def is_insert_mode(self):
        return self.current_mode == "i"

    def is_terminal_mode(self):
        return self.current_mode == "t"

    def get_active_mode(self):
        title = ui.active_window().title
        mode = None
        if "MODE:" in title:
            mode = title.split("MODE:")[1].split(" ")[0]
            if mode not in self.vim_modes.keys():
                return None
            self.current_mode = mode
        return mode

    # XXX - not used currently
    def get_active_rpc(self):
        title = ui.active_window().title
        if "RPC" in title:
            named_pipe = title.split("RPC:")[1].split(" ")[0]
            return named_pipe
        return None

    def current_mode_id(self):
        if self.is_normal_mode():
            return self.NORMAL
        elif self.is_visual_mode():
            return self.VISUAL
        elif self.is_insert_mode():
            return self.INSERT
        elif self.is_terminal_mode():
            return self.TERMINAL

    def set_normal_mode(self, auto=True):
        self.adjust_mode(self.NORMAL, auto=auto)

    def set_normal_mode_exterm(self):
        self.adjust_mode(self.NORMAL, escape_terminal=True)

    # XXX - fix the auto stuff, maybe have separate method version or something

    # XXX - should np imply exterm? as not preserving is a fairly big
    # operation?
    def set_normal_mode_np(self, auto=True):
        self.adjust_mode(self.NORMAL, no_preserve=True, auto=auto)

    def set_visual_mode(self):
        self.adjust_mode(self.VISUAL)

    def set_visual_mode_np(self):
        self.adjust_mode(self.VISUAL, no_preserve=True)

    def set_insert_mode(self):
        self.adjust_mode(self.INSERT)

    def set_terminal_mode(self):
        self.adjust_mode(self.TERMINAL)

    def set_any_motion_mode(self):
        self.adjust_mode([self.NORMAL, self.VISUAL])

    def set_any_motion_mode_np(self):
        self.adjust_mode(self.NORMAL, no_preserve=True)

    def adjust_mode(
        self, valid_mode_ids, no_preserve=False, escape_terminal=False, auto=True
    ):
        if auto is True and settings.get("user.vim_adjust_modes") == 0:
            return

        cur = self.current_mode_id()
        # print("Current mode is {}".format(cur))
        if type(valid_mode_ids) != list:
            valid_mode_ids = [valid_mode_ids]
        if cur not in valid_mode_ids:
            # Just favor the first mode
            self.set_mode(
                valid_mode_ids[0],
                no_preserve=no_preserve,
                escape_terminal=escape_terminal,
            )

    # Often I will say `delete line` and it will trigger `@delete` and `@nine`.
    # This then keys 9. I then say `undo` to fix the bad delete, which does 9
    # undos. Chaos ensues... the seeks to fix that
    def cancel_queued_commands(self):
        if (
            settings.get("user.vim_cancel_queued_commands") == 1
            and self.is_normal_mode()
        ):
            print("escaping queued cmd")
            actions.key("escape")
            timeout = settings.get("user.vim_cancel_queued_commands_timeout")
            time.sleep(timeout)

    # XXX - should switch this to neovim RPC when available
    # for now we simply use keyboard binding combinations
    def set_mode(self, wanted_mode, no_preserve=False, escape_terminal=False):
        current_mode = self.get_active_mode()

        if current_mode == wanted_mode or (
            self.is_terminal_mode() and wanted_mode == self.INSERT
        ):
            return

        timeout = settings.get("user.vim_mode_change_timeout")
        # print("Setting mode to {}".format(wanted_mode))
        # enter normal mode where necessary
        if self.is_terminal_mode():
            if (
                settings.get("user.vim_escape_terminal_mode") is True
                or escape_terminal is True
            ):
                # break out of terminal mode
                actions.key("ctrl-\\")
                actions.key("ctrl-n")
            else:
                # Imagine you have a vim terminal and inside you're running a
                # terminal that is using vim mode rather than emacs mode. This
                # means you will want to be able to use some amount of vim
                # commands to edit the shells command line itself without
                # actually being inside the encapsulating vim instance.
                # The use of escape here tries to compensate for those
                # scenerios, where you won't break into the encapsulating vim
                # instance. Needs to be tested. If you don't like this, you can
                # set vim_escape_terminal_mode to 1
                actions.key("escape")
                time.sleep(timeout)
        elif self.is_insert_mode():
            if (
                wanted_mode == self.NORMAL
                and no_preserve is False
                and settings.get("user.vim_preserve_insert_mode") >= 1
            ):
                # XXX - make this a configurable option
                actions.key("ctrl-\\")  # don't move the cursor on mode switch
                actions.key("ctrl-o")
            else:
                # Presses right because entering normal mode via escape puts
                # the cursor back one position, otherwise misaligns on words.
                # Exception is `2 delete big-back` from INSERT mode.
                actions.key("right")
                actions.key("escape")

            time.sleep(timeout)
        elif self.is_visual_mode():
            actions.key("escape")
            time.sleep(timeout)

        # switch to explicit mode if necessary
        if wanted_mode == self.INSERT:
            actions.key("i")
        # or just let the original 'mode' command run from this point
        elif wanted_mode == self.VISUAL:
            # first we cancel queued normal commands that might mess with 'v'
            # ex: normal mode press 5, then press v to switch to visual
            actions.key("escape")
            actions.key("v")

        # Here we assume we are now in some normalized state:
        # need to make the notify command configurable
        if settings.get("user.vim_notify_mode_changes") >= 1:
            self.notify_mode_change(wanted_mode)
            ...

    def notify_mode_change(self, mode):
        """Function to be customized by talon user to determine how they want
        notifications on mode changes"""
        # .system_command('notify-send.sh -t 3000 "{} mode"'.format(mode))
        pass
