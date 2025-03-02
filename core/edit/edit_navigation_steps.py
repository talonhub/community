from contextlib import suppress
from dataclasses import dataclass
from typing import Callable, Literal

from talon import Module, actions, settings


@dataclass
class NavigationStep:
    modifier: Literal[
        "wordLeft", "wordRight", "word", "left", "right", "lineUp", "lineDown"
    ]
    count: int


mod = Module()


@mod.capture(rule="[<number_small>] {user.edit_modifier_repeatable}")
def navigation_step(m) -> NavigationStep:
    count = 1
    modifier = m.edit_modifier_repeatable

    with suppress(AttributeError):
        count = m.number_small

    return NavigationStep(
        modifier=modifier,
        count=count,
    )


@mod.action_class
class Actions:
    def perform_navigation_steps(steps: list[NavigationStep]):
        """Navigate by a series of steps"""
        for step in steps:
            match step.modifier:
                case "wordLeft":
                    repeat_action(actions.edit.word_left, step.count, True)
                case "wordRight":
                    repeat_action(actions.edit.word_right, step.count, True)
                case "word":
                    repeat_action(actions.edit.word_right, step.count, True)
                case "left":
                    repeat_action(actions.edit.left, step.count)
                case "right":
                    repeat_action(actions.edit.right, step.count)
                case "lineUp":
                    repeat_action(actions.edit.up, step.count)
                case "lineDown":
                    repeat_action(actions.edit.down, step.count)


def repeat_action(action: Callable, count: int, delay: bool = False):
    delay_string = None

    if delay:
        delay_string = f"{settings.get('user.edit_command_word_selection_delay')}ms"

    for _ in range(count):
        action()

        if delay_string:
            actions.sleep(delay_string)
