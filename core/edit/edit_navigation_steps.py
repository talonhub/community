from contextlib import suppress
from dataclasses import dataclass
from typing import Callable, Literal

from talon import Module, actions


@dataclass
class NavigationStep:
    type: Literal["wordLeft", "wordRight", "word", "left", "right", "lineUp", "lineDown"]
    count: int


mod = Module()


@mod.capture(rule="[<number_small>] {user.edit_modifier_repeatable}")
def navigation_step(m) -> NavigationStep:
    type = "character"
    count = 1

    with suppress(AttributeError):
        type = m.edit_modifier_repeatable

    with suppress(AttributeError):
        count = m.number_small

    return NavigationStep(
        type=type,
        count=count,
    )


@mod.action_class
class Actions:
    def perform_navigation_steps(steps: list[NavigationStep]):
        """Navigate by a series of steps"""
        for step in steps:
            match step.type:
                case "wordLeft":
                     repeat_action(actions.edit.word_left, step.count)
                case "wordRight":
                    repeat_action(actions.edit.word_right, step.count)
                case "word":
                    repeat_action(actions.edit.word_right, step.count)
                case "left":
                    repeat_action(actions.edit.left, step.count)
                case "right":
                    repeat_action(actions.edit.right, step.count)
                case "lineUp":
                    repeat_action(actions.edit.up, step.count)
                case "lineDown":
                    repeat_action(actions.edit.down, step.count)


def repeat_action(action: Callable, count: int):
    for _ in range(count):
        action()
