from talon import Context, Module, actions, ui

mod = Module()
mod.tag("draft_editor_active", "Indicates whether the draft editor has been activated")
mod.tag(
    "draft_editor_app_focused",
    "Indicates that the draft editor app currently has focus",
)

ctx = Context()
tags: set[str] = set()


def add_tag(tag: str):
    tags.add(tag)
    ctx.tags = list(tags)


def remove_tag(tag: str):
    tags.discard(tag)
    ctx.tags = list(tags)


default_names = ["Visual Studio Code", "Code", "VSCodium", "Codium", "code-oss"]

setting_editor_names = mod.setting(
    "draft_editor",
    type=str,
    default=None,
    desc="List of application names to use for draft editor",
)


def get_editor_names():
    names_csv = setting_editor_names.get()
    return names_csv.split(", ") if names_csv else default_names


@mod.scope
def scope():
    editor_names = get_editor_names()

    for app in ui.apps(background=False):
        if app.name in editor_names:
            return {"draft_editor_running": True}

    return {"draft_editor_running": False}


def handle_app_activate(app):
    if app.name in get_editor_names():
        add_tag("user.draft_editor_app_focused")
    else:
        remove_tag("user.draft_editor_app_focused")


ui.register("app_launch", scope.update)
ui.register("app_close", scope.update)
ui.register("app_activate", handle_app_activate)


original_window = None

last_draft = None


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
        add_tag("user.draft_editor_active")

    def draft_editor_submit():
        """Submit/save draft editor"""
        close_editor(submit_draft=True)

    def draft_editor_discard():
        """Discard draft editor"""
        close_editor(submit_draft=False)

    def draft_editor_paste_last():
        """Paste last submitted draft"""
        if last_draft:
            actions.user.paste(last_draft)


def get_editor_app() -> ui.App:
    editor_names = get_editor_names()

    for app in ui.apps(background=False):
        if app.name in editor_names:
            return app

    raise RuntimeError("Draft editor is not running")


def close_editor(submit_draft: bool):
    global last_draft
    remove_tag("user.draft_editor_active")
    actions.edit.select_all()
    selected_text = actions.edit.selected_text()
    actions.edit.delete()
    actions.app.tab_close()
    actions.user.switcher_focus_window(original_window)
    actions.sleep("300ms")
    if submit_draft:
        last_draft = selected_text
        actions.user.paste(selected_text)
