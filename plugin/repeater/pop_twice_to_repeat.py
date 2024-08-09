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


@ctx.action_class("user")
class UserActions:
    def noise_trigger_pop():
        # Since zoom mouse is registering against noise.register("pop", on_pop), let that take priority
        if actions.tracking.control_zoom_enabled():
            return
        global time_last_pop
        delta = time.perf_counter() - time_last_pop
        double_pop_speed_minimum = settings.get("user.double_pop_speed_minimum")
        double_pop_speed_maximum = settings.get("user.double_pop_speed_maximum")
        if delta >= double_pop_speed_minimum and delta <= double_pop_speed_maximum:
            actions.core.repeat_command()
        time_last_pop = time.perf_counter()
