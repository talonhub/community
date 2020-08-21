from talon import Context, actions, ui, Module, app

# from user.knausj_talon.code.snippet_watcher import snippet_watcher
import os

ctx = Context()
ctx.matches = r"""
app: vscode
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


# def update_list(watch_list):
#     ctx.lists["user.snippets"] = watch_list


# # there's probably a way to do this without
# # if app.platform == "windows":
# watcher = snippet_watcher(
#     {os.path.expandvars(r"%AppData%\Code\User\snippets"): ["csharp.json"],},
#     update_list,
# )

# print("reloaded!")
