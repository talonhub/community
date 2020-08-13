from talon import Context, actions, ui, Module, app

ctx = Context()
ctx.matches = r"""
app: Code
app: Code - OSS
app: Code
app: Visual Studio Code
app: Code.exe
mode: user.python
mode: command 
and code.language: python
"""
# short name -> ide clip name
ctx.lists["user.snippets"] = {
    "class funky": "def(class method)",
    "class static funky": "def(class static method)",
    "class": "class",
    "else if": "elif",
    "for": "for",
    "funky": "def",
    "if else": "if/else",
    "if": "if",
    "lambda": "lambda",
    "try except": "try/except",
    "while": "while",
    "with": "with",
}
