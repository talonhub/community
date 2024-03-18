import time

from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()

mod.tag("pop_twice_to_repeat", desc="tag for enabling pop twice to repeat")

ctx.matches = r"""
mode: command
and tag: user.pop_twice_to_repeat
"""

time_last_pop = 0
double_pop_speed_minimum = settings.get("user.double_pop_speed_minimum")  # default 0.1
double_pop_speed_maximum = settings.get("user.double_pop_speed_maximum")  # defualt 0.3


@ctx.action_class("user")
class UserActions:
    def noise_trigger_pop():
        global time_last_pop
        delta = time.time() - time_last_pop
        if delta >= double_pop_speed_minimum and delta <= double_pop_speed_maximum:
            actions.core.repeat_command()
        time_last_pop = time.time()
