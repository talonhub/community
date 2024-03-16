import time

from talon import Context, actions, Module

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


@ctx.action_class("user")
class UserActions:
    def noise_trigger_pop():
        global time_last_pop
        delta = time.time() - time_last_pop
        if delta >= 0.1 and delta <= 0.3:
            actions.core.repeat_command()
        time_last_pop = time.time()
