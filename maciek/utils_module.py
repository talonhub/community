from talon import Context, actions, ui, Module, app

mod = Module()


@mod.action_class
class Actions:
    def maybe_sleep(miliseconds: int, text: str):
        """this description is mandatory"""
        if len(text) > 0:
            actions.sleep(miliseconds)

    def go_up(n: int):
        """This description is mandatory"""
        for i in range(n):
            actions.edit.up()

    def go_down(n: int):
        """This description is mandatory"""
        for i in range(n):
            actions.edit.down()
