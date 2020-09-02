from talon import Context, Module, actions, clip

ctx = Context()
mod = Module()


def get_selected_text(default=None):
    try:
        with clip.capture() as s:
            actions.edit.copy()
        return s.get()
    except clip.NoChange:
        return clip.get()


@ctx.action_class("edit")
class edit_actions:
    def selected_text() -> str:
        selected_text = get_selected_text()
        return selected_text or ""


@mod.action_class
class Actions:
    def paste(text: str):
        """Pastes text and preserves clipboard"""
        with clip.revert():
            clip.set(text)
            actions.edit.paste()
