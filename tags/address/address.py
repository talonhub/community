from talon import Module

mod = Module()
mod.tag(
    "address",
    desc="Application with a mechanism to browse or navigate by address; e.g., an address bar or Finder's go-to-folder functionality",
)


@mod.capture
def address(m) -> str:
    """Captures an address; this capture must be implemented in the context which desires to support the grammar"""


@mod.action_class
class Actions:
    def address_focus():
        """Focuses the address input field"""

    def address_copy_address():
        """Copies the current address"""

    def address_navigate(address: str):
        """Navigates to the desired address"""
