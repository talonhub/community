# see doc/vim.md
# XXX - define all the lists separately and then update ctx.lists only once
# XXX - document that visual selection mode implies terminal escape
# XXX - eventually use nvim RPC to confirm mode changes vs relying on a time
#       delay that is buggy depending on your cpu consumption
# XXX - add setting for disabling local terminal escape when running inside
#       remote vim sessions via ssh, etc
# XXX - import and test scenario where the mode isn't listed at all
# XXX - add test cases
# XXX - simplify a bunch of the lists name

import time

from talon import Context, Module, actions, settings, ui

try:
    import pynvim

    has_pynvim = True
except Exception:
    has_pynvim = False

mod = Module()
ctx = Context()

ctx.matches = r"""
win.title:/VIM/
"""


# Based on you using a custom title string like this:
# see doc/vim.md
@ctx.action_class("win")
class win_actions:
    def filename():
        title = actions.win.title()
        result = title.split(")")
        # Assumes the last word after the last ) entry has the filename
        if len(result) > 1:
            result = result[-1]
        # print(result)
        if "." in result:
            return result
        return ""

    def file_ext():
        ext = actions.win.filename().split(".")[-1]
        # print(ext)
        return ext


ctx.lists["self.vim_arrow"] = {
    "left": "h",
    "right": "l",
    "up": "k",
    "down": "j",
}

# XXX - need to break into normal, visual, etc
# XXX - Technically some of these are not counted atm... so could be split
# Standard self.vim_counted_actions insertable entries
standard_counted_actions = {
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
    "erase": "x",
    "erase reversed": "X",
    "erase back": "X",
    #    "put": "p",
    "put below": "p",
    "paste": "p",
    "paste below": "p",
    "put before": "P",
    "paste before": "P",
    "put above": "P",
    "paste above": "P",
    "repeat": ".",
    "indent line": ">>",
    # Warning saying unindent line is painful
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
    "upper case line": "gUU",
    "lower case line": "guu",
    # XXX - these work from visual mode and normal mode
    "insert before": "I",
    "insert line": "I",
    "play again": "@@",
    "toggle case": "~",
    "repeat last swap": "&",
    # XXX - not sure how to name these
    "delete rest": "D",
    "delete remaining": "D",
    "change rest": "C",
    "change remaining": "C",
}

# Standard self.vim_counted_actions key() entries
standard_counted_actions_control_keys = {
    "redo": "ctrl-r",
    "scroll down": "ctrl-f",
    "scroll up": "ctrl-b",
    "page down": "ctrl-f",
    "page up": "ctrl-b",
    "half page down": "ctrl-d",
    "half scroll down": "ctrl-d",
    "half page up": "ctrl-u",
    "half scroll up": "ctrl-u",
    "increment": "ctrl-a",
    "decrement": "ctrl-x",
}

# Custom self.vim_counted_actions insertable entries
# You can put custom aliases here to make it easier to manage. The idea is to
# alias commands from standard_counted_actions above, without replacing them
# there to prevent merge conflicts.
custom_counted_action = {
    "panic": "u",
    "dine": "dd",
    "drop": "x",
    "yine": "Y",
    "slide left": "<<",
    "slide right": ">>",
}

# Custom self.vim_counted_actions insertable entries
# You can put custom shortcuts requiring key() here to make it easier to manage
custom_counted_actions_control_keys = {}

ctx.lists["self.vim_counted_actions"] = {
    **standard_counted_actions,
    **custom_counted_action,
}

ctx.lists["self.vim_counted_actions_keys"] = {
    **standard_counted_actions_control_keys,
    **custom_counted_actions_control_keys,
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
# with an existing global context talon media grammar
ctx.lists["self.vim_counted_actions_args"] = {
    "play macro": "@",  # takes char arg
}

# normal mode commands that require motion, and that are counted
# includes motions and no motions :|
commands_with_motion = {
    # no motions
    "join": "J",
    "filter": "=",  # XXX - not sure about how to use this
    # "put": "p",
    "paste": "p",
    "undo": "u",
    "swap case": "~",
    # motions
    "change": "c",
    "delete": "d",
    "trim": "d",  # XXX - because talent doesn't like my "delete"
    "indent": ">",
    "unindent": "<",
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
    "trim": "d",  # XXX - because talon doesn't like the way I say "delete"
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
}


ctx.lists["self.vim_motion_commands"] = list(
    set().union(commands_with_motion.keys(), visual_commands.keys())
)

vim_motions = {
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
    "back big end": "gE",
    "right": "l",
    "left": "h",
    "down": "j",
    "up": "k",
    "next": "n",
    "next reversed": "N",
    "previous": "N",
    "column zero": "0",
    "column": "|",
    "start of line": "^",
    "bend": "^",
    "end of line": "$",
    "lend": "$",
    "cursor search": "*",
    "curse search": "*",
    "cursor search reversed": "#",
    "curse search reversed": "#",
    # These conflict with general 'search' command
    # "search under cursor": "*",
    # "search under cursor reversed": "#",
    "again": ";",
    "again reversed": ",",
    "down sentence": ")",
    "sentence": ")",
    "up sentence": "(",
    "down paragraph": "}",
    "paragraph": "}",
    "up paragraph": "{",
    "start of next section": "]]",
    "next section": "]]",
    "start of previous section": "[[",
    "previous section": "[[",
    # XXX - next section end??
    "end of next section": "][",
    # XXX - previous section end??
    "end of previous section": "[]",
    # XXX - not sure about naming - don't seem to work yet
    "block end": "]}",
    "block start": "[{",
    "previous block": "[}",
    "matching": "%",
    "down line": "+",
    "up line": "-",
    "first character": "_",
    "cursor home": "H",
    "curse home": "H",
    "cursor top": "H",
    "curse top": "H",
    "cursor middle": "M",
    "curse middle": "M",
    "cursor last": "L",
    "curse last": "L",
    "cursor bottom": "L",
    "curse bottom": "L",
    "start of document": "gg",
    "start of file": "gg",
    "top of document": "gg",
    "top of file": "gg",
    "end of document": "G",
    "end of file": "G",
}

vim_motions_custom = {
    "function start": "[[",
    "funk start": "[[",
    "next function": "]]",
    "next funk": "]]",
}

ctx.lists["self.vim_motions"] = {
    **vim_motions,
    **vim_motions_custom,
}


# XXX - make easier to say
ctx.lists["self.vim_motions_keys"] = {
    "last cursor": "ctrl-o",
    "forward cursor": "ctrl-i",
    "retrace movements": "ctrl-o",
    "retrace movements forward": "ctrl-i",
}

# all of these motions take a character argument
vim_motions_with_character = {
    "jump to mark": "'",
    "find": "f",
    "find reversed": "F",
    "find previous": "F",
    "till": "t",
    "till reversed": "T",
    "till previous": "T",
}

# NOTE: these will not work with the surround plug in, since they combo
# commands.
# XXX - Also breaks with insert preserving. ctrl-o ^ reverts, so f* is inserted
# need a way to fix that up
custom_vim_motions_with_character_commands = {
    "last": "$F",  # find starting end of line
    "first": "^f",  # find starting beginning of line
}

ctx.lists["self.vim_motions_with_character"] = {
    **vim_motions_with_character,
    **custom_vim_motions_with_character_commands,
}


# all of these motions take a phrase argument
ctx.lists["self.vim_motions_with_phrase"] = {
    "search": "/",
    "search reversed": "?",
}

ctx.lists["self.vim_text_object_range"] = {
    "inner": "i",
    "inside": "i",
    "around": "a",
    "this": "a",
}

# Common names used for text object selection, vim-surround, etc
common_key_names = {
    "tick": "'",
    "quote": '"',
}


# XXX - Should match more wording in vim_surround_targets
text_object_select = {
    "word": "w",
    "words": "w",
    "big word": "W",
    "big words": "W",
    "block": "b",
    "blocks": "b",
    "big block": "B",
    "big blocks": "B",
    "dubquote": '"',
    "dub quote": '"',
    "double quotes": '"',
    "quote": "'",
    "single quotes": "'",
    "ticks": "'",
    "parens": "(",
    "parenthesis": "(",
    "angle brackets": "<",
    "angles": "<",
    # These are pluralized because of how you speak vim grammars
    # ex: yank inside braces
    "curly braces": "{",
    "code block": "{",
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

text_object_select_custom = {}

ctx.lists["self.vim_text_object_select"] = {
    **text_object_select,
    **text_object_select_custom,
}

# Specific to the vim-surround plugin
# XXX - should be able to partially mix with earlier list
ctx.lists["self.vim_surround_targets"] = {
    "stars": "*",
    "asterisks": "*",
    "word": "w",
    "big word": "W",
    "block": "b",
    "big block": "B",
    "string": '"',
    # "dub string": '"',
    # "dub quotes": '"',
    "quotes": '"',
    "double quotes": '"',
    # "quotes": "'",
    "ticks": "'",
    # "string": "'",
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

# settings that you can just set by sing on or off
# correlates to settings that start with no in turning off
vim_on_and_off_settings = {
    "see indent": "cindent",
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

mod.setting(
    "vim_mode_switch_moves_cursor",
    type=int,
    default=0,
    desc="Preserving insert mode will automatically move the cursor. Setting this to 0 can override that.",
)

mod.setting(
    "vim_use_rpc",
    type=int,
    default=0,
    desc="Whether or not to use RPC if it is available. Useful for testing or avoiding bugs",
)
mod.setting(
    "vim_debug", type=int, default=0, desc="Debugging used for development",
)


# Standard VIM motions and action
mod.list("vim_arrow", desc="All vim direction keys")
mod.list("vim_motion_commands", desc="Counted VIM commands with motions")
# mod.list("vim_counted_motions", desc="Counted VIM motion verbs")
mod.list("vim_counted_actions", desc="Counted VIM action verbs")
mod.list("vim_counted_actions_keys", desc="Counted VIM action verbs ctrl keys")
mod.list("vim_normal_counted_action", desc="Normal counted VIM actions")
mod.list("vim_normal_counted_actions_keys", desc="Counted VIM action verbs ctrl keys")
mod.list("vim_motions", desc="Non-counted VIM motions")
mod.list("vim_motions_keys", desc="Non-counted VIM motions ctrl keys")
mod.list("vim_motions_with_character", desc="VIM motion verbs with char arg")
mod.list("vim_motions_with_phrase", desc="VIM motion verbs with phrase arg")
mod.list("vim_motions_all", desc="All VIM motion verbs")
mod.list("vim_text_object_range", desc="VIM text object ranges")
mod.list("vim_text_object_select", desc="VIM text object selections")
mod.list("vim_jump_range", desc="VIM jump ranges")
mod.list("vim_jumps", desc="VIM jump verbs")
mod.list("vim_jump_targets", desc="VIM jump targets")
mod.list("vim_normal_counted_motion_command", desc="Counted normal VIM commands")
mod.list("vim_counted_motion_command_with_ordinals", desc="Counted normal VIM commands")
mod.list("vim_select_motion", desc="VIM visual mode selection motions")
mod.list("vim_any", desc="All vim commands")

# Plugin-specific lists
mod.list("vim_surround_targets", desc="VIM surround plugin targets")

# Plugin modes
mod.mode("vim_fugitive", desc="A fugitive mode that exposes git mappings")


@mod.capture
def vim_arrow(m) -> str:
    "An arrow direction to be converted to vim direction"
    return m.vim_arrow


@mod.capture
def vim_surround_targets(m) -> str:
    "Returns a text object used by the surround plugin"


@mod.capture
def vim_select_motion(m) -> str:
    "Returns a string"


@mod.capture
def vim_counted_actions(m) -> str:
    "Returns a string"


@mod.capture
def vim_counted_actions_keys(m) -> str:
    "Returns a string"


@mod.capture
def vim_normal_counted_action(m) -> str:
    "Returns a string"


@mod.capture
def vim_normal_counted_actions_keys(m) -> str:
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
def vim_text_object_range(m) -> str:
    "Returns a string"


@mod.capture
def vim_text_object_select(m) -> str:
    "Returns a string"


@mod.capture
def vim_motion_commands(m) -> str:
    "Returns a list of verbs"


# @mod.capture
# def vim_counted_motions(m) -> str:
#    "Returns a list of verbs"


@mod.capture
def vim_motions(m) -> str:
    "Returns a list of verbs"


@mod.capture
def vim_motions_keys(m) -> str:
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


@mod.capture
def vim_counted_motion_command_with_ordinals(m) -> str:
    "Returns a string"


@mod.capture
def vim_normal_counted_motion_keys(m) -> str:
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


@ctx.capture(rule="{self.vim_motions}")
def vim_motions(m) -> str:
    return m.vim_motions


@ctx.capture(rule="{self.vim_motions_keys}")
def vim_motions_keys(m) -> str:
    return m.vim_motions_keys


@ctx.capture(
    rule="{self.vim_motions_with_character} (ship|upper|uppercase) <user.letter>"
)
def vim_motions_with_upper_character(m) -> str:
    return m.vim_motions_with_character + "".join(list(m)[2:]).upper()


@ctx.capture(
    rule="{self.vim_motions_with_character} (<user.letter>|<digits>|<user.symbol>)"
)
def vim_motions_with_character(m) -> str:
    return m.vim_motions_with_character + "".join(str(x) for x in list(m)[1:])


@ctx.capture(rule="{self.vim_motions_with_phrase} <user.text>")
def vim_motions_with_phrase(m) -> str:
    return "".join(list(m.vim_motions_with_phrase + m.text))


@ctx.capture(
    rule="(<self.vim_motions>|<self.vim_motions_with_character>|<self.vim_motions_with_upper_character>|<self.vim_motions_with_phrase>)"
)
def vim_motions_all(m) -> str:
    return "".join(list(m))


@ctx.capture(
    rule="(<self.vim_motions>|<self.vim_motions_with_character>|<self.vim_motions_with_upper_character>|<self.vim_motions_with_phrase>)"
)
def vim_motions_all_adjust(m) -> str:
    v = VimMode()
    v.set_any_motion_mode()
    print(m)
    return "".join(list(m))


@ctx.capture(rule="{self.vim_counted_actions}")
def vim_counted_actions(m) -> str:
    return m.vim_counted_actions


@ctx.capture(rule="{self.vim_counted_actions_keys}")
def vim_counted_actions_keys(m) -> str:
    return m.vim_counted_actions_keys


# @ctx.capture(rule="[<number_small>] <self.vim_motions_all>")
# def vim_counted_motions(m) -> str:
#    return "".join(str(x) for x in list(m))


@ctx.capture(rule="{self.vim_jump_range}")
def vim_jump_range(m) -> str:
    return m.vim_jump_range


@ctx.capture(rule="{self.vim_jumps}")
def vim_jumps(m) -> str:
    return m.vim_jumps


@ctx.capture(rule="{self.vim_surround_targets}")
def vim_surround_targets(m) -> str:
    return m.vim_surround_targets


@ctx.capture(rule="<self.vim_jump_range> <self.vim_jumps>")
def vim_jump_targets(m) -> str:
    return "".join(list(m))


@ctx.capture(
    # XXX - trying to reduce list sizes and never use this
    # rule="[<number_small>] <self.vim_text_object_range> <self.vim_text_object_select>"
    rule="<self.vim_text_object_range> <self.vim_text_object_select>"
)
def vim_text_objects(m) -> str:
    return "".join(str(x) for x in list(m))


# Sometimes you want to imply a surround action is going to work on a word, but
# saying around is tedious, of this is defaults to selecting around if no
# actual inner or around range is spoken
@ctx.capture(rule="[<number_small>] <self.vim_text_object_select>")
def vim_unranged_surround_text_objects(m) -> str:
    if len(list(m)) == 1:
        return "a" + "".join(list(m))
    else:
        return "".join(str(m.number_small)) + "a" + "".join(list(m)[1:])


@ctx.capture(rule="{self.vim_motion_commands}")
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
        return ""

    v.set_normal_mode()
    return commands_with_motion[str(m)]


@ctx.capture(
    rule="[<number_small>] <self.vim_motion_commands> [(<self.vim_motions_all> | <self.vim_text_objects> | <self.vim_jump_targets>)]"
)
def vim_normal_counted_motion_command(m) -> str:
    return "".join(str(x) for x in list(m))


@ctx.capture(
    rule="<self.vim_motion_commands> <user.ordinals> (<self.vim_motions_all>|<self.vim_jump_targets>)"
)
def vim_counted_motion_command_with_ordinals(m) -> str:
    return "".join([str(m.ordinals - 1), "".join(m[2:]), m[0], "".join(m[2:])])


@ctx.capture(rule="[<number_small>] <self.vim_motions_keys>")
def vim_normal_counted_motion_keys(m) -> str:
    # we do this because we pass everything to key() which needs a space
    # separated list
    if len(str(m).split(" ")) > 1:
        return " ".join(list((" ".join(list(str(m.number_small))), m.vim_motions_keys)))
    else:
        return m.vim_motions_keys


# XXX - could combine actions_keys and _action version by test if the entry is
# in which list. might reduce number usage?
@ctx.capture(rule="[<number_small>] <self.vim_counted_actions>")
def vim_normal_counted_action(m) -> str:
    # XXX - may need to do action-specific mode checking
    v = VimMode()
    v.cancel_queued_commands()
    if m.vim_counted_actions == "u":
        # undo doesn't work with ctrl-o it seems
        v.set_any_motion_mode_np()
    else:
        v.set_any_motion_mode()

    return "".join(str(x) for x in list(m))


@ctx.capture(rule="[<number_small>] <self.vim_counted_actions_keys>")
def vim_normal_counted_actions_keys(m) -> str:
    v = VimMode()
    v.cancel_queued_commands()
    v.set_any_motion_mode()

    # we do this because repass everything to key() which needs a space
    # separated list
    if len(str(m).split(" ")) > 1:
        return " ".join(
            list((" ".join(list(str(m.number_small))), m.vim_counted_actions_keys))
        )
    else:
        return m.vim_counted_actions_keys


@ctx.capture(
    rule="[<number_small>] (<self.vim_motions> | <self.vim_text_objects> | <self.vim_jump_targets>)"
)
def vim_select_motion(m) -> str:
    return "".join(str(x) for x in list(m))


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

    def vim_set_visual_line_mode():
        """set visual line mode"""
        v = VimMode()
        v.set_visual_line_mode()

    def vim_set_visual_block_mode():
        """set visual block mode"""
        v = VimMode()
        v.set_visual_block_mode()

    def vim_set_insert_mode():
        """set insert mode"""
        v = VimMode()
        v.set_insert_mode()

    def vim_set_terminal_mode():
        """set terminal mode"""
        v = VimMode()
        v.set_terminal_mode()

    def vim_set_command_mode():
        """set visual mode"""
        v = VimMode()
        v.set_command_mode()

    def vim_set_command_mode_exterm():
        """set visual mode"""
        v = VimMode()
        v.set_command_mode_exterm()

    def vim_insert_mode(cmd: str):
        """run a given list of commands in normal mode, preserve mode"""
        v = VimMode()
        v.set_insert_mode()
        actions.insert(cmd)

    def vim_insert_mode_key(cmd: str):
        """run a given list of commands in normal mode, preserve mode"""
        v = VimMode()
        v.set_insert_mode()
        actions.key(cmd)

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

    def vim_normal_mode_exterm_preserve(cmd: str):
        """run a given list of commands in normal mode, escape from terminal
        mode, but return to terminal mode after. Special case for settings"""
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

    # technically right now they run in in normal mode, but these calls will
    # ensure that any queued commands are removed
    def vim_command_mode(cmd: str):
        """run a given list of commands in command mode, preserve INSERT"""
        v = VimMode()
        v.set_command_mode()
        actions.insert(cmd)

    # technically right now they run in in normal mode, but these calls will
    # ensure that any queued commands are removed
    def vim_command_mode_exterm(cmd: str):
        """run a given list of commands in command mode, preserve INSERT"""
        v = VimMode()
        v.set_command_mode_exterm()
        actions.insert(cmd)

    # Sometimes the .talon file won't know what mode to run something in, just
    # that it needs to be a mode that supports motions like normal and visual.
    def vim_any_motion_mode(cmd: str):
        """run a given list of commands in normal mode"""
        v = VimMode()
        v.set_any_motion_mode()
        actions.insert(cmd)

    # Sometimes the .talon file won't know what mode to run something in, just
    # that it needs to be a mode that supports motions like normal and visual.
    def vim_any_motion_mode_exterm(cmd: str):
        """run a given list of commands in some motion mode"""
        v = VimMode()
        v.set_any_motion_mode_exterm()
        actions.insert(cmd)

    def vim_any_motion_mode_key(cmd: str):
        """run a given list of commands in normal mode"""
        v = VimMode()
        v.set_any_motion_mode()
        actions.key(cmd)

    def vim_any_motion_mode_exterm_key(cmd: str):
        """run a given list of commands in normal mode"""
        v = VimMode()
        v.set_any_motion_mode_exterm()
        actions.key(cmd)


class NeoVimRPC:
    """For setting/pulling the modes using RPC"""

    def __init__(self):
        self.init_ok = False
        self.nvim = None

        if settings.get("user.vim_use_rpc") == 0:
            return

        self.rpc_path = self.get_active_rpc()
        if self.rpc_path is not None:
            try:
                self.nvim = pynvim.attach("socket", path=self.rpc_path)
            except RuntimeError:
                return
            self.init_ok = True
        else:
            return

    def get_active_rpc(self):
        title = ui.active_window().title
        if "RPC" in title:
            named_pipe = title.split("RPC:")[1].split(" ")[0]
            return named_pipe
        return None

    def get_active_mode(self):
        mode = self.nvim.request("nvim_get_mode")
        return mode


class VimNonRpc:
    """For pulling the modes out of the title string, if RPC isn't
    available. Is generally slower.."""

    pass


class VimMode:
    # mode ids represent generic statusline mode() values. see :help mode()
    NORMAL = 1
    VISUAL = 2
    VISUAL_LINE = 3
    VISUAL_BLOCK = 4
    INSERT = 5
    TERMINAL = 6
    COMMAND = 7
    REPLACE = 8
    VREPLACE = 9

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
        self.nvrpc = NeoVimRPC()
        self.current_mode = self.get_active_mode()

    def dprint(self, s):
        if settings.get("user.vim_debug"):
            print(s)

    def is_normal_mode(self):
        return self.current_mode == "n"

    def is_visual_mode(self):
        return self.current_mode in ["v", "V", "^V"]

    def is_insert_mode(self):
        return self.current_mode == "i"

    def is_terminal_mode(self):
        return self.current_mode == "t"

    def is_command_mode(self):
        return self.current_mode == "c"

    def is_replace_mode(self):
        return self.current_mode in ["R", "Rv"]

    def get_active_mode(self):
        if self.nvrpc.init_ok is True:
            mode = self.nvrpc.get_active_mode()["mode"]
            # XXX -
            self.current_mode = mode
        else:
            title = ui.active_window().title
            mode = None
            if "MODE:" in title:
                mode = title.split("MODE:")[1].split(" ")[0]
                self.dprint(mode)
                if mode not in self.vim_modes.keys():
                    return None
                self.current_mode = mode

        return mode

    def current_mode_id(self):
        if self.is_normal_mode():
            return self.NORMAL
        elif self.is_visual_mode():
            return self.VISUAL
        elif self.is_insert_mode():
            return self.INSERT
        elif self.is_terminal_mode():
            return self.TERMINAL
        elif self.is_command_mode():
            return self.COMMAND

    def set_normal_mode(self, auto=True):
        self.adjust_mode(self.NORMAL, auto=auto)

    def set_normal_mode_exterm(self):
        self.adjust_mode(self.NORMAL, escape_terminal=True)

    # XXX - revisit auto, maybe have separate method version or something
    def set_normal_mode_np(self, auto=True):
        self.adjust_mode(self.NORMAL, no_preserve=True, auto=auto)

    def set_visual_mode(self):
        self.adjust_mode(self.VISUAL)

    def set_visual_mode_np(self):
        self.adjust_mode(self.VISUAL, no_preserve=True)

    def set_visual_line_mode(self):
        self.adjust_mode(self.VISUAL_LINE)

    def set_visual_block_mode(self):
        self.adjust_mode(self.VISUAL_BLOCK)

    def set_insert_mode(self):
        self.adjust_mode(self.INSERT)

    def set_terminal_mode(self):
        self.adjust_mode(self.TERMINAL)

    def set_command_mode(self):
        self.adjust_mode(self.COMMAND)

    def set_command_mode_exterm(self):
        self.adjust_mode(self.COMMAND, escape_terminal=True)

    def set_replace_mode(self):
        self.adjust_mode(self.REPLACE)

    def set_visual_replace_mode(self):
        self.adjust_mode(self.VREPLACE)

    def set_any_motion_mode(self):
        self.adjust_mode([self.NORMAL, self.VISUAL])

    def set_any_motion_mode_exterm(self):
        self.adjust_mode([self.NORMAL, self.VISUAL], escape_terminal=True)

    def set_any_motion_mode_np(self):
        self.adjust_mode(self.NORMAL, no_preserve=True)

    def adjust_mode(
        self, valid_mode_ids, no_preserve=False, escape_terminal=False, auto=True
    ):
        if auto is True and settings.get("user.vim_adjust_modes") == 0:
            return

        self.get_active_mode()
        cur = self.current_mode_id()
        if type(valid_mode_ids) != list:
            valid_mode_ids = [valid_mode_ids]
        self.dprint(f"from {cur} to {valid_mode_ids}")
        if cur not in valid_mode_ids:
            # Just favor the first mode match
            self.set_mode(
                valid_mode_ids[0],
                no_preserve=no_preserve,
                escape_terminal=escape_terminal,
            )

    # Often I will say `delete line` and it will trigger `@delete` and `@nine`.
    # This then keys 9. I then say `undo` to fix the bad delete, which does 9
    # undos. Chaos ensues... this seeks to fix that
    def cancel_queued_commands(self):
        if (
            settings.get("user.vim_cancel_queued_commands") == 1
            and self.is_normal_mode()
        ):
            # print("escaping queued cmd")
            actions.key("escape")
            timeout = settings.get("user.vim_cancel_queued_commands_timeout")
            time.sleep(timeout)

    def wait_mode_change(self, wanted):
        timeout = settings.get("user.vim_mode_change_timeout")
        if self.nvrpc.init_ok:
            while wanted != self.nvrpc.get_active_mode()["mode"][0]:
                print("%s vs %s" % (wanted, self.nvrpc.get_active_mode()["mode"]))
                time.sleep(0.01)
        else:
            time.sleep(timeout)

    # XXX - should switch this to neovim RPC when available. note however, it
    # appears neovim api doesn't support programmatic mode switching, only
    # querying. also querying certain modes is broken (^V mode undetected)
    # for now we simply use keyboard binding combinations
    def set_mode(self, wanted_mode, no_preserve=False, escape_terminal=False):
        current_mode = self.get_active_mode()

        if current_mode == wanted_mode or (
            self.is_terminal_mode() and wanted_mode == self.INSERT
        ):
            return

        # print("Setting mode to {}".format(wanted_mode))
        # enter normal mode where necessary
        if self.is_terminal_mode():
            if (
                settings.get("user.vim_escape_terminal_mode") is True
                or escape_terminal is True
            ):
                # print("escaping")
                # break out of terminal mode
                actions.key("ctrl-\\")
                actions.key("ctrl-n")
                self.wait_mode_change("n")
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
                # NOTE: do not wait on mode change here, as we
                # cannot detect it for the inner thing
        elif self.is_insert_mode():
            if (
                wanted_mode == self.NORMAL
                and no_preserve is False
                and settings.get("user.vim_preserve_insert_mode") >= 1
            ):
                if settings.get("user.vim_mode_switch_moves_cursor") == 0:
                    actions.key("ctrl-\\")  # don't move the cursor on mode switch
                actions.key("ctrl-o")
            else:
                # Presses right because entering normal mode via escape puts
                # the cursor back one position, otherwise misaligns on words.
                # Exception is `2 delete big-back` from INSERT mode.
                actions.key("right")
                actions.key("escape")
            self.wait_mode_change("n")
        elif self.is_visual_mode() or self.is_command_mode() or self.is_replace_mode():
            actions.key("escape")
            self.wait_mode_change("n")
        elif self.is_normal_mode() and wanted_mode == self.COMMAND:
            # We explicitly escape even if normal mode, to cancel any queued
            # commands that might affect our command. For instance, accidental
            # number queueing followed by :w, etc
            actions.key("escape")
            self.wait_mode_change("n")

        # switch to explicit mode if necessary
        if wanted_mode == self.INSERT:
            actions.key("i")
        # or just let the original 'mode' command run from this point
        elif wanted_mode == self.VISUAL:
            # first we cancel queued normal commands that might mess with 'v'
            # ex: normal mode press 5, then press v to switch to visual
            actions.key("escape")
            actions.key("v")
        elif wanted_mode == self.VISUAL_LINE:
            # first we cancel queued normal commands that might mess with 'v'
            # ex: normal mode press 5, then press v to switch to visual
            actions.key("escape")
            actions.key("V")
        elif wanted_mode == self.VISUAL_BLOCK:
            # first we cancel queued normal commands that might mess with 'v'
            # ex: normal mode press 5, then press v to switch to visual
            actions.key("escape")
            actions.key("ctrl-v")
        elif wanted_mode == self.COMMAND:
            # XXX - could check cmd to see if it has the ':' and if not have
            # this func set it
            pass
        elif wanted_mode == self.REPLACE:
            actions.key("R")
        elif wanted_mode == self.VREPLACE:
            actions.key("g R")

        # Here we assume we are now in some normalized state:
        # need to make the notify command configurable
        if settings.get("user.vim_notify_mode_changes") >= 1:
            self.notify_mode_change(wanted_mode)
            ...

    def notify_mode_change(self, mode):
        """Function to be customized by talon user to determine how they want
        notifications on mode changes"""
        pass
