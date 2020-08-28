from talon import Context, actions, ui, Module, app

# from user.knausj_talon.code.snippet_watcher import snippet_watcher
import os

ctx = Context()
ctx.matches = r"""
app: vscode
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


def update_list(watch_list):
    ctx.lists["user.snippets"] = watch_list


# there's probably a way to do this without
# if app.platform == "windows":
# watcher = snippet_watcher(
#     {os.path.expandvars(r"%AppData%\Code\User\snippets"): ["python.json"],},
#     update_list,
# )

