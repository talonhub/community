# define the spoken forms for symbols in command and dictation mode
punctuation_dict = {}

# for dragon, we add a couple of mappings that don't work for conformer
# i.e. dragon supports some actual symbols as the spoken form
dragon_punctuation_dict = {
    "`": "`",
    ",": ",",
}

# define the spoken forms for symbols that are intended for command mode only
symbol_key_dict = {}

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

symbols = [
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
symbols.extend(currency_symbols)

for symbol in symbols:
    if symbol.command_and_dictation_forms:
        for spoken_form in symbol.command_and_dictation_forms:
            punctuation_dict[spoken_form] = symbol.character
            symbol_key_dict[spoken_form] = symbol.character
            dragon_punctuation_dict[spoken_form] = symbol.character

    if symbol.command_forms:
        for spoken_form in symbol.command_forms:
            symbol_key_dict[spoken_form] = symbol.character
