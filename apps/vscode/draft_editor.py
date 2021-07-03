from talon import Module, actions, ui
import time

mod = Module()
active_window = None
editor = None


@mod.action_class
class Actions:
    def draft_editor_open():
        """Open draft jump"""
        global active_window, editor
        active_window = ui.active_window()
        has_selected_text = actions.edit.selected_text() != ""
        if has_selected_text:
            actions.edit.copy()
        actions.user.switcher_focus("Code")
        new_file()
        if has_selected_text:
            actions.edit.paste()

    def draft_editor_save():
        """Save draft jump"""
        global active_window, editor
        if not active_window:
            return
        actions.edit.select_all()
        actions.edit.copy()
        close_file()
        focus_window(active_window)
        actions.edit.paste()
        active_window = None
        editor = None

    def draft_editor_discard():
        """Discard draft jump"""
        global active_window, editor
        if not active_window:
            return

        close_file()
        focus_window(active_window)

        active_window = None
        editor = None


def get_editor():
    editor_names = {"Visual Studio Code", "Code", "VSCodium", "Codium", "code-oss"}
    for w in ui.windows():
        if w.app.name in editor_names:
            return w
    raise RuntimeError("VSCode is not running")


def new_file():
    actions.user.vscode("workbench.action.files.newUntitledFile")


def close_file():
    actions.edit.select_all()
    actions.edit.delete()
    actions.app.tab_close()


def focus_window(window):
    window.focus()
    t1 = time.monotonic()
    while ui.active_window() != window:
        if time.monotonic() - t1 > 5:
            raise RuntimeError("Can't focus window")
        actions.sleep("50ms")
    actions.sleep("200ms")