from talon import Module, actions

# --- Tag definition ---
mod = Module()
mod.tag("chapters", desc="Reader app with chapter navigation")


# --- Define actions ---
@mod.action_class
class Actions:
    def chapter_current() -> int:
        """Return current chapter number"""

    def chapter_next():
        """Go to next chapter"""
        actions.user.chapter_jump(actions.user.chapter_current() + 1)

    def chapter_previous():
        """Go to previous chapter"""
        actions.user.chapter_jump(actions.user.chapter_current() - 1)

    def chapter_jump(number: int):
        """Go to chapter number"""

    def chapter_final():
        """Go to final chapter"""
