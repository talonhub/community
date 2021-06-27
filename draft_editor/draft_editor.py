from talon import Module, actions, ui
import time

mod = Module()
mod.mode("draft_editor", "Mode to show if the draft editor is open")

active_window = None

@mod.action_class
class Actions:
    def draft_editor_open():
        """Open draft editor"""
        global active_window
        active_window = ui.active_window()
        editor = get_editor()
        has_selected_text = actions.edit.selected_text() != ""
        if has_selected_text:
            actions.edit.copy()
        focus_window(editor)
        new_file()
        if has_selected_text:
            actions.edit.paste()
        actions.mode.enable("user.draft_editor")

    def draft_editor_save():
        """Save draft editor"""
        close_editor(True)

    def draft_editor_discard():
        """Discard draft editor"""
        close_editor(False)


def close_editor(save: bool):
    actions.mode.disable("user.draft_editor")
    actions.edit.select_all()
    if save:
        actions.edit.copy()
    close_file()
    focus_window(active_window)
    if save:
        actions.edit.paste()

def get_editor():
    editor_names = {
        "Visual Studio Code",
        "Code",
        "VSCodium",
        "Codium",
        "code-oss"
    }
    for w in ui.windows():
        if w.app.name in editor_names:
            return w
    raise RuntimeError("VSCode is not running")

def new_file():
    actions.user.vscode("workbench.action.files.newUntitledFile")

def close_file():
    actions.edit.delete()
    actions.app.tab_close()

def focus_window(window: ui.Window):
    """Focus window and wait until finished"""
    window.focus()
    t1 = time.monotonic()
    while ui.active_window() != window:
        if time.monotonic() - t1 > 1:
            raise RuntimeError(f"Can't focus window: {window.title}")
        actions.sleep("50ms")
