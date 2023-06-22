from talon import Module, actions

# --- Tag definition ---
mod = Module()
mod.tag("pages", desc="Anything with page navigation")


# --- Define actions ---
@mod.action_class
class Actions:
    def page_current() -> int:
        """Return current page number"""

    def page_next():
        """Go to next page"""
        actions.user.page_jump(actions.user.page_current() + 1)

    def page_previous():
        """Go to previous page"""
        actions.user.page_jump(actions.user.page_current() - 1)

    def page_jump(number: int):
        """Go to page number"""

    def page_final():
        """Go to final page"""
