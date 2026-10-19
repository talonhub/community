# fmt: off

from talon import Context, Module, actions

from ..user_settings import track_csv_rows

ctx = Context()

ctx_dragon = Context()
ctx_dragon.matches = r"""
speech.engine: dragon
"""

# define the spoken forms for symbols in command and dictation mode
punctuation_dict = {}

# define spoken form for symbols for use in create_spoken_forms.py functionality
# we define a handful of symbol only. at present, this is restricted to one entry per symbol.
symbols_for_create_spoken_forms = {
    # for application names like "Movies & TV"
    "and": "&",
    # for emails
    "at": "@",
    "dot": ".",
    # for application names like "notepad++"
    "plus": "+",
}

# this class is kept for backwards compatibility with people's Community forks
# symbols defined with this are used for the default symbols.csv only
class Symbol:
    character: str
    command_and_dictation_forms: list[str] = None
    command_forms: list[str] = None

    def __init__(
        self, character: str, command_and_dictation_forms=None, command_forms=None
    ):
        self.character = character

        if command_and_dictation_forms:
            self.command_and_dictation_forms = (
                [command_and_dictation_forms]
                if isinstance(command_and_dictation_forms, str)
                else command_and_dictation_forms
            )

        if command_forms:
            self.command_forms = (
                [command_forms] if isinstance(command_forms, str) else command_forms
            )

currency_symbols = [
    Symbol("$", ["dollar sign"]),
    # Symbol("£", ["pound sign"], ["pound"]),
]

old_symbols = [
    Symbol("`", ["brick"]),
    Symbol(",", ["comma", "coma", "kama", "spama"]),
    Symbol(".", ["period", "point"]),
    Symbol(";", ["semi"]),
    Symbol(":", ["stack"]),
    Symbol("/", ["stroke"]),
    Symbol("?", ["quest"]),
    Symbol("!", ["bang"]),
    Symbol("*", ["snow"]),
    Symbol("#", ["pound"]),
    Symbol("%", ["percy"]),
    Symbol("@", ["at sign"]),
    Symbol("&", ["amper"]),
    Symbol("-", ["dash"]),
    Symbol("=", ["equal"]),
    Symbol("+", ["plus"]),
    Symbol("~", ["tilde"]),
    Symbol("_", ["score"]),
    Symbol("(", ["leper"]),
    Symbol(")", ["repper"]),
    Symbol("[", ["lacker"]),
    Symbol("]", ["racker"]),
    Symbol("\\", ["backstroke"]),
    Symbol("{", ["lacer"]),
    Symbol("}", ["racer"]),
    Symbol("<", ["langle"]),
    Symbol(">", ["wrangle"]),
    Symbol("^", ["tangle"]),
    Symbol("|", ["piper"]),
    Symbol("'", ["single"]),
    Symbol('"', ["double"]),
    Symbol(" ", ["void"]),
]

# by convention, symbols should include currency symbols
old_symbols.extend(currency_symbols)

default_symbols = []
for symbol in old_symbols:
    if symbol.command_and_dictation_forms:
        command_and_dictation_row = [symbol.character, "both"]
        command_and_dictation_row.extend(symbol.command_and_dictation_forms)
        default_symbols.append(command_and_dictation_row)
    if symbol.command_forms:
        command_row = [symbol.character, "command"]
        command_row.extend(symbol.command_forms)
        default_symbols.append(command_row)

@track_csv_rows("symbols.csv", headers=("Symbol", "Mode (command/dictation/both)", "Spoken Forms (separated with commas)"), default=default_symbols)
def on_symbols(values):
    # define the spoken forms for symbols that are intended for command mode only
    symbol_key_dict = {}
    # for command and dictation mode
    punctuation_dict.clear()
    # for dragon, we add a couple of mappings that don't work for conformer
    # i.e. dragon supports some actual symbols as the spoken form
    dragon_punctuation_dict = {
        "`": "`",
        ",": ",",
    }
    for i, row in enumerate(values):
        # tolerate a blank line
        if len(row) == 0 or (len(row) == 1 and row[0].isspace()):
            continue
        if len(row) < 3:
            warning = f"Row {i+1} of symbols.csv did not have enough columns!"
            print(warning)
            actions.app.notify(warning)
            continue
        symbol = row[0].strip()
        mode = row[1].strip()
        spoken_forms = [s.strip() for s in row[2:]]
        if mode == "command" or mode == "both":
            for spoken_form in spoken_forms:
                symbol_key_dict[spoken_form] = symbol
        if mode == "dictation" or mode == "both":
            for spoken_form in spoken_forms:
                punctuation_dict[spoken_form] = symbol
                dragon_punctuation_dict[spoken_form] = symbol
        if mode not in ("command", "dictation", "both"):
            warning = f"Row {i+1} of symbols.csv has mode not used by the symbol support {mode}!"
            print(warning)
            actions.app.notify(warning)
    ctx.lists["user.punctuation"] = punctuation_dict
    ctx.lists["user.symbol_key"] = symbol_key_dict
    ctx_dragon.lists["user.punctuation"] = dragon_punctuation_dict

mod = Module()
@mod.action_class
class Actions:
    def get_punctuation_words():
        """Gets the user.punctuation list"""
        return punctuation_dict
