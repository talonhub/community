from talon import Module, Context, actions

# --- App definition ---
mod = Module()
mod.apps.calibre_viewer = """
app: calibre
title: /E-book viewer$/
title: /eBook-Betrachter$/
"""

# Context matching
ctx = Context()
ctx.matches = """
os: windows
os: linux
app: calibre_viewer
"""
# TODO: mac implementation


# --- Implement actions ---
@ctx.action_class("user")
class UserActions:
    # user.pages
    def page_next(): actions.key("pagedown")
    def page_previous(): actions.key("pageup")
    def page_final(): actions.key("ctrl-end")
    # user.chapters
    def chapter_next(): actions.key("ctrl-pagedown")
    def chapter_previous(): actions.key("ctrl-pageup")
