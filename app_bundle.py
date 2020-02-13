from talon import clip, ui
from talon.voice import Context

context = Context("bundle")

context.keymap({"copy [app] bundle": lambda m: clip.set(ui.active_app().bundle)})
