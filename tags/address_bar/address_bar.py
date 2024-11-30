from talon import Module

mod = Module()
mod.tag("address_bar", desc="Application with address bar")


@mod.capture
def address(m) -> str:
    """Captures an address; this capture must be implemented the context which desires to support the grammar"""


@mod.action_class
class Actions:
    def address_bar_focus():
        """Focuses the address bar"""

    def address_bar_copy_address():
        """Copies the current address"""

    def address_bar_navigate(address: str):
        """Navigates to the desired address"""
