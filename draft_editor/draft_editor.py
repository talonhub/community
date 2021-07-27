from talon import Module, actions, ui, app
import time

mod = Module()
mod.mode("draft_editor", "Indicates whether the draft editor has been activated")

default_names = [
    "Visual Studio Code",
    "Code",
    "VSCodium",
    "Codium",
    "code-oss"
]

setting_editor_names = mod.setting(
    "draft_editor",
    type=str,
    default=None,
    desc="List of application names to use for draft editor",
)

editor_names = {}


@mod.scope
def scope():
    for app in ui.apps(background=False):
        if app.name in editor_names:
            return {"draft_editor_running": True}
    return {"draft_editor_running": False}


def on_ready():
    global editor_names
    names_csv = setting_editor_names.get()
    editor_names = names_csv.split(", ") if names_csv else default_names

    names_str = '\n'.join({f"app.name: {name}" for name in editor_names})
    mod.apps.draft_editor = f"""{names_str}"""

    ui.register("app_launch", scope.update)
    ui.register("app_close", scope.update)


app.register("ready", on_ready)


original_window = None


@mod.action_class
class Actions:
    def draft_editor_open():
        """Open draft editor"""
        global original_window
        original_window = ui.active_window()
        editor_app = get_editor_app()
        selected_text = actions.edit.selected_text()
        actions.user.switcher_focus_app(editor_app)
        # Wait additional time for talon context to update.
        actions.sleep("200ms")
        actions.app.tab_open()
        if selected_text != "":
            actions.user.paste(selected_text)
        actions.mode.enable("user.draft_editor")

    def draft_editor_submit():
        """Submit/save draft editor"""
        close_editor(submit_draft=True)

    def draft_editor_discard():
        """Discard draft editor"""
        close_editor(submit_draft=False)


def get_editor_app() -> ui.App:
    for app in ui.apps(background=False):
        if app.name in editor_names:
            return app
    raise RuntimeError("Draft editor is not running")


def close_editor(submit_draft: bool):
    actions.mode.disable("user.draft_editor")
    actions.edit.select_all()
    selected_text = actions.edit.selected_text()
    actions.edit.delete()
    actions.app.tab_close()
    actions.user.switcher_focus_window(original_window)
    if submit_draft:
        actions.user.paste(selected_text)
