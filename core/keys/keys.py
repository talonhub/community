from talon import Context, Module, actions, app
from .symbols import symbols_command_and_dictation, symbols_command, dragon_symbols_command_and_dictation

mod = Module()
ctx = Context()

ctx_dragon = Context()
ctx_dragon = Context()
ctx_dragon.matches = r"""
speech.engine: dragon
"""

mod.list("letter", desc="The spoken phonetic alphabet")
mod.list("symbol_key", desc="All symbols from the keyboard")
mod.list("arrow_key", desc="All arrow keys")
mod.list("number_key", desc="All number keys")
mod.list("modifier_key", desc="All modifier keys")
mod.list("function_key", desc="All function keys")
mod.list("special_key", desc="All special keys")
mod.list("keypad_key", desc="All keypad keys")
mod.list("punctuation", desc="words for inserting punctuation into text")


@mod.capture(rule="{self.modifier_key}+")
def modifiers(m) -> str:
    "One or more modifier keys"
    return "-".join(m.modifier_key_list)


@mod.capture(rule="{self.arrow_key}")
def arrow_key(m) -> str:
    "One directional arrow key"
    return m.arrow_key


@mod.capture(rule="<self.arrow_key>+")
def arrow_keys(m) -> str:
    "One or more arrow keys separated by a space"
    return str(m)


@mod.capture(rule="{self.number_key}")
def number_key(m) -> str:
    "One number key"
    return m.number_key


@mod.capture(rule="{self.keypad_key}")
def keypad_key(m) -> str:
    "One keypad key"
    return m.keypad_key


@mod.capture(rule="{self.letter}")
def letter(m) -> str:
    "One letter key"
    return m.letter


@mod.capture(rule="{self.special_key}")
def special_key(m) -> str:
    "One special key"
    return m.special_key


@mod.capture(rule="{self.symbol_key}")
def symbol_key(m) -> str:
    "One symbol key"
    return m.symbol_key


@mod.capture(rule="{self.function_key}")
def function_key(m) -> str:
    "One function key"
    return m.function_key


@mod.capture(rule="( <self.letter> | <self.number_key> | <self.symbol_key> )")
def any_alphanumeric_key(m) -> str:
    "any alphanumeric key"
    return str(m)


@mod.capture(
    rule="( <self.letter> | <self.number_key> | <self.symbol_key> "
    "| <self.arrow_key> | <self.function_key> | <self.special_key> | <self.keypad_key>)"
)
def unmodified_key(m) -> str:
    "A single key with no modifiers"
    return str(m)


@mod.capture(rule="{self.modifier_key}* <self.unmodified_key>")
def key(m) -> str:
    "A single key with optional modifiers"
    try:
        mods = m.modifier_key_list
    except AttributeError:
        mods = []
    return "-".join(mods + [m.unmodified_key])


@mod.capture(rule="<self.key>+")
def keys(m) -> str:
    "A sequence of one or more keys with optional modifiers"
    return " ".join(m.key_list)


@mod.capture(rule="{self.letter}+")
def letters(m) -> str:
    "Multiple letter keys"
    return "".join(m.letter_list)

@mod.action_class
class Actions:
    def get_punctuation_words():
        """Gets the user.punctuation list"""
        return symbols_command_and_dictation

ctx.lists["self.punctuation"] = symbols_command_and_dictation
ctx.lists["self.symbol_key"] = symbols_command
ctx_dragon.lists["self.symbol_key"] = dragon_symbols_command_and_dictation
