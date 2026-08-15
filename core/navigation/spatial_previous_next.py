from talon import Module, actions

mod = Module()
mod.list(
    "spatial_previous_next", desc="Canonical spatial previous/next direction word"
)


@mod.capture(rule="{user.spatial_previous_next}")
def spatial_previous_next(m) -> str:
    """A spatial previous/next direction word, returns PREV or NEXT"""
    return m.spatial_previous_next


@mod.action_class
class Actions:
    def key_spatial_previous_next(direction: str, key_prev: str, key_next: str):
        """Press key_prev or key_next depending on direction (PREV/NEXT)"""
        actions.key(key_prev if direction == "PREV" else key_next)
