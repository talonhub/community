# define the spoken forms for symbols in command and dictation mode
symbols_command_and_dictation = {}

# for dragon, we add a couple of mappings that don't work for conformer
# i.e. dragon supports some actual symbols as the spoken form
dragon_symbols_command_and_dictation = {
    "`": "`",
    ",": ",",
}

# define the spoken forms for symbols that are intended for dictation mode only
symbols_dictation = {}

# define spoken form for symbols for use in create_spoken_forms.py functionality
# we define a handful of symbol only. at present, this is restricted to one entry per symbol.
symbols_for_create_spoken_forms = {
    # for application names like "Movies & TV"
    "and": "&",
    # for emails
    "at": "@",
    "dot": ".",
    # for application names like "notepad++"
    "plus": "+"
}

class Symbol:
    character: str
    dictation_forms: list[str] = None
    command_and_dictation_forms: list[str] = None

    def __init__(self, character: str, command_and_dictation_forms: str | list[str] = None, dictation_forms: str | list[str] = None):
        if len(character) != 1:
            raise ValueError(f"character must be a single character, got: '{character}'")
        
        self.character = character
        
        if command_and_dictation_forms:
            self.command_and_dictation_forms = (
                [command_and_dictation_forms] if isinstance(command_and_dictation_forms, str) else command_and_dictation_forms
            )

        if dictation_forms:
            self.dictation_forms = (
                [dictation_forms] if isinstance(dictation_forms, str) else dictation_forms
            )

currency_symbols = [
    Symbol("$", ["dollar"]),
    Symbol("£", ["pound sign"]),
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
            symbols_command_and_dictation[spoken_form] = symbol.character
            symbols_dictation[spoken_form] = symbol.character
            dragon_symbols_command_and_dictation[spoken_form] = symbol.character

    if symbol.dictation_forms:
        for spoken_form in symbol.dictation_forms:
            symbols_dictation[spoken_form] = symbol.character
            dragon_symbols_command_and_dictation[spoken_form] = symbol.character
