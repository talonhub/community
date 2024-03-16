import time

from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()

mod.tag("pop_twice_to_wake", desc="tag for enabling pop twice to wake in sleep mode")

mod.setting(
    "double_pop_speed_minimum",
    type=float,
    desc="""Shortest time in seconds to accept a second pop to trigger additional actions""",
    default=0.1,
)

mod.setting(
    "double_pop_speed_maximum",
    type=float,
    desc="""Longest time in seconds to accept a second pop to trigger additional actions""",
    default=0.3,
)

ctx.matches = r"""
mode: sleep
and tag: user.pop_twice_to_wake
"""

time_last_pop = 0
double_pop_speed_minimum = settings.get(
    "user.double_pop_speed_minimum"
)  # default 0.1
double_pop_speed_maximum = settings.get(
    "user.double_pop_speed_maximum"
)  # default 0.3


@ctx.action_class("user")
class UserActions:
    def noise_trigger_pop():
        global time_last_pop
        delta = time.time() - time_last_pop
        if delta >= last_pop_time_minimum and delta <= last_pop_time_maximum:
            actions.speech.enable()
        time_last_pop = time.time()
