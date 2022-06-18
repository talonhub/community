from talon import Context

# from user.knausj_talon.code.snippet_watcher import snippet_watcher

ctx = Context()
ctx.matches = r"""
app: vscode
tag: user.csharp
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
# snippet_path = None
# if app.platform == "windows":
#     snippet_path = os.path.expandvars(r"%AppData%\Code\User\snippets")
# elif app.platform == "mac":
#     snippet_path = os.path.expanduser(
#         "~/Library/Application Support/Code/User/snippets"
#     )
# if snippet_path:
#     watcher2 = snippet_watcher({snippet_path: ["csharp.json",],}, update_list,)
# print("reloaded!")
