from talon import Module, actions

mod = Module()
mod.tag("address_bar", desc="Application with address bar")

@mod.capture
def address(m) -> str:
    """Captures an address"""

@mod.action_class
class Actions:
    def address_bar_focus():
        """Focuses the address bar"""

    def address_bar_copy_address():
        """Copies the current address"""

    def address_bar_navigate(address: str):
        """Navigates to the desired address"""
