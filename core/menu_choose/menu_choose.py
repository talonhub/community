from talon import Context, Module, actions

mod = Module()


@mod.action_class
class Actions:
    def choose(number_small: int):
        """Choose the nth item"""
        actions.key(f"down:{number_small-1} enter")

    def choose_up(number_small: int):
        """Choose the nth item up"""
        actions.key(f"up:{number_small} enter")
