from talon import Context, actions, ui, Module, app

ctx = Context()
ctx.matches = r"""
app: Code
app: Code - OSS
app: Code
app: Visual Studio Code
app: Code.exe
mode: user.csharp
mode: command 
and code.language: csharp
"""
# short name -> ide clip name
ctx.lists["user.snippets"] = {
    "class": "class",
    "else": "else",
    "for each": "foreach",
    "if": "if",
    "try except": "try",
    "try finally": "tryf",
    "while": "while",
    # "class funky": "def(class method)",
    # "class static funky": "def(class static method)",
    # "for": "for",
    # "funky": "def",
}
