import time

from talon import Context, actions, Module, settings

ctx = Context()
mod = Module()

mod.tag(
    "pop_twice_to_repeat",
    desc="tag for enabling pop twice to repeat"
)

ctx.matches = r"""
mode: command
and tag: user.pop_twice_to_repeat
"""

time_last_pop = 0
last_pop_time_minimum = settings.get("user.mouse_enable_pop_stops_scroll") # default 0.1
last_pop_time_maximum = settings.get("user.mouse_enable_pop_stops_scroll") # defualt 0.3

@ctx.action_class("user")
class UserActions:
    def noise_trigger_pop():
        global time_last_pop
        delta = time.time() - time_last_pop
        if delta >= last_pop_time_minimum and delta <= last_pop_time_maximum:
            actions.core.repeat_command()
        time_last_pop = time.time()
