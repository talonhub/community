from talon import Context, Module, actions, ctrl, settings, ui

mod = Module()
ctx_global = Context()

@ctx_global.action_class("deck")
class DeckActions:
    def goto(serial: str, path: str):
        if path in ["control", "zoom"]:
            actions.user.deck_cache_path("A00SA3232MA4OZ")

        actions.next(serial, path)
