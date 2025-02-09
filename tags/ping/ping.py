from talon import Module

mod = Module()
mod.tag(
    "ping",
    desc="Enables commands for applications of support tagging a particular person",
)

@mod.capture
def ping(m) -> str:
    """The user to ping"""

@mod.action_class
class Actions:
    def ping(address: str):
        """Pings the desired user"""
