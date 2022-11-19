from talon import Context, actions, ui, Module, app

ctx = Context()
ctx.matches = """
os:mac
and title:/knausj_talon/
"""

ctx.lists["user.file_shortcuts"] = {
    "code": "vscode.talon",
    "code pie": "vscode.py",
    "knaus": "knausj.py",
    "keys": "keys.py",
    "global": "maciek/mac_global.talon",
    "chrome": "maciek/chrome_mac.talon",
    "command": "maciek/commandline.talon",
    "Taskfile":"Taskfile.yml",
    "replace":"settings/words_to_replace.csv",
    "websites":"websites.csv",
    "talon settings":"settings.talon"
    
}

