from talon import Context, actions, ui, Module, app

ctx = Context()
ctx.matches = r'''
app: Code
app: Code - OSS
app: Code
app: Visual Studio Code
app: Code.exe
mode: user.python
mode: command 
and code.language: python
'''
#short name -> ide clip name
ctx.lists["user.snippets"] = {
    "funky": "def",
    "for": "for",
    "while": "while",
    "class": "class",
    "class funky": "def(class method)",
    "class static funky": "def(class static method)",
    "with": "with",
    "if": "if",
    "if else": "if/else",
    "else if": "elif",
    "lambda": "lambda",
    "try except": "try/except",
}
