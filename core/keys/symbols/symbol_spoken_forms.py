from .symbol import Symbol

# for dragon, we add a couple of mappings that don't work for conformer
# i.e. dragon supports some actual symbols as the spoken form
dragon_symbols = {
    "`": "`",
    ",": ",",
}

# define the spoken forms for symbols that are intended for command mode only
symbols = {}

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

currency_symbols = [
    Symbol("$", ["dollar"]),
    Symbol("£", ["pound sign"]),
]

symbols_definitions = [
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
symbols_definitions.extend(currency_symbols)

# build the spoken form maps
for symbol in symbols_definitions:
    if symbol.spoken_forms:
        for spoken_form in symbol.spoken_forms:
            symbols[spoken_form] = symbol.character
            dragon_symbols[spoken_form] = symbol.character