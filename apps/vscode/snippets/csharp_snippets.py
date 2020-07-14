from talon import Context, actions, ui, Module, app

ctx = Context()
ctx.matches = r'''
app: Code
app: Code - OSS
app: Code
app: Visual Studio Code
app: Code.exe
mode: user.csharp
mode: command 
and code.language: csharp
'''
#short name -> ide clip name
ctx.lists["user.snippets"] = {
    #"funky": "def",
    #"for": "for",
    "for each": "foreach",
    "while": "while",
    "class": "class",
    #"class funky": "def(class method)",
    #"class static funky": "def(class static method)",
    "if": "if",
    "else": "else",
    "try except": "try",
    "try finally": "tryf"
}