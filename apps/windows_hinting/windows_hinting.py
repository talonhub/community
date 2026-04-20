from talon import Context, Module, app, ui
mod = Module()
ctx = Context()
ctx_win = Context()
ctx_win.matches = r"""
os: windows
"""

@ctx_win.capture("user.hinting_double", rule="<user.letter> (twice | second)")
def hinting_double(m) -> str:
    return f"{m.letter} {m.letter}"

@ctx_win.capture("user.hinting", rule="<user.letter> | <user.letter> <user.letter> | <user.hinting_double> ")
def hinting(m) -> str:
    return " ".join(m)

is_window_hinting_active = False
@mod.scope
def scope():
    return {"windows_hinting_active": f"{is_window_hinting_active}"}

def on_title(win):
    global is_window_hinting_active
    if win.app.name == "Windows-Hinting":
        if "[Active]" in win.title:
            is_window_hinting_active = True
        else:
            is_window_hinting_active = False

        scope.update()

def on_ready():
    ui.register("win_title", on_title)

app.register("ready", on_ready)